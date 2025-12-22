from paths import get_app_dir, get_vault_path
from storage import get_vault, write_vault
from encryption import encrypt_vault, decrypt_vault

def vault_exists() -> bool:
    return get_vault_path().exists()

def create_vault(email: str, masterpass: str):
    if vault_exists():
       raise FileExistsError("Vault already exists") 
    
    vault = {}

    encrypted_vault = encrypt_vault(email,masterpass,vault)

    write_vault(encrypted_vault)

def load_vault(email: str, masterpass: str):
    if not vault_exists():
        raise FileNotFoundError("Vault file does not exist")
    
    vault_bytes = get_vault()

    vault = decrypt_vault(email,masterpass,vault_bytes)

    return vault

if __name__ == '__main__':
    print(load_vault("email@example.com","masterpass6"))
