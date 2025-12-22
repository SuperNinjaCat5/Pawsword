from Pawsword.paths import get_app_dir, get_vault_path
from Pawsword.storage import get_vault, write_vault
from Pawsword.encryption import encrypt_vault, decrypt_vault

def vault_exists() -> bool:
    return get_vault_path().exists()

def create_vault(email: str, masterpass: str):
    if vault_exists():
       raise FileExistsError("Vault already exists") 
    
    vault = {}

    encrypted_vault = encrypt_vault(email,masterpass,vault)

    write_vault(encrypted_vault)

def load_vault(email: str, masterpass: str) -> dict:
    if not vault_exists():
        raise FileNotFoundError("Vault file does not exist")
    
    vault_bytes = get_vault()

    vault = decrypt_vault(email,masterpass,vault_bytes)

    return vault

def save_vault(email: str, masterpass: str, vault: dict):

    if not vault_exists():
        create_vault(email,masterpass)

    try:
        current_vault = load_vault(email,masterpass)
    except FileNotFoundError:
        current_vault = {}

    if vault == current_vault:
        raise ValueError("Vault unchanged, nothing to save")
  
    encrypted_vault = encrypt_vault(email,masterpass,vault)

    write_vault(encrypted_vault)
    
def add_entry(email: str, masterpass: str, service: str, username: str, password: str):
    vault = load_vault(email,masterpass)

    if service in vault:
        raise ValueError(f"Service {service} already exists in the vault")
        
    vault[service] = {"username": username, "password": password}

    save_vault(email,masterpass,vault)

def remove_entry(email: str, masterpass: str, service: str):
    vault = load_vault(email,masterpass)

    if service not in vault:
        raise ValueError(f"Service {service} does not exist in the vault")
        
    del vault[service]

    save_vault(email,masterpass,vault)

def get_entry(email: str, masterpass: str, service: str):
    vault = load_vault(email,masterpass)

    if service not in vault:
        raise ValueError(f'No entry found for service {service}')
    
    return vault[service]

def list_services(email: str, masterpass: str) -> list:
    return list(load_vault(email, masterpass).keys())

if __name__ == '__main__':
    email = "email@example.com"
    masterpass = "masterpass6"

    create_vault(email,masterpass)

    # add_entry(email,masterpass,"Fortnite","fnCOOLLLLL","dontStealMyVbuck6769")

    # print(get_entry(email,masterpass,"Fortnite"))

    # remove_entry(email,masterpass,"Fortnite")