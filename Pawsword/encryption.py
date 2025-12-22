from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import json

def encrypt_vault(email: str,masterpass: str,json_to_encrypt: dict) -> bytes:
    vault_key = f"{email}|{masterpass}".encode()

    salt = os.urandom(16) # makes random 16 bytes of data
    
    kdf = Scrypt( # this is what you are supposed to use I guess, it will encrypt stuff more randomly than jst pass
        salt=salt,# your random bytes
        length=32, # lenght of key
        n=2**14, # i dont rlly know
        r=8, # !!
        p=1 # math?
    )

    key = kdf.derive(vault_key)
    nonce = os.urandom(12) # makes random 12 bytes of data
    
    aesgcm = AESGCM(key)

    vault_json = json.dumps(json_to_encrypt)

    vault_bytes = vault_json.encode()

    encryped_data = aesgcm.encrypt(nonce,vault_bytes,associated_data=None)

    return salt + nonce + encryped_data

def decrypt_vault(email: str,masterpass: str,full_encrypted_data: bytes) -> dict:
    salt = full_encrypted_data[:16] # first 16 bytes is salt
    nonce = full_encrypted_data[16:28] # next 12 bytes is nonce
    encrypted_data = full_encrypted_data[28:] # everything else

    vault_key = f"{email}|{masterpass}".encode()

    kdf = Scrypt( # get same kdf
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1 
    )

    key = kdf.derive(vault_key) # get same vault key

    aesgcm = AESGCM(key) # get same AESGCM

    decrypted_data = aesgcm.decrypt(nonce,encrypted_data,associated_data=None)

    return json.loads(decrypted_data.decode()) # returns as json