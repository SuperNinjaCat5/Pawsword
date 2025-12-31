from Pawsword.paths import get_vault_path

def get_vault():
    vault_path = get_vault_path()

    if not vault_path.exists():
        raise FileNotFoundError("Vault file does not exist")
    
    return vault_path.read_bytes()

def write_vault(data):
    vault_path = get_vault_path()

    temp_path = vault_path.with_suffix(".tmp") # Writes the stuff on a temp path so if stuff dies then you don't lose passwords amd stuff

    temp_path.write_bytes(data)

    temp_path.replace(vault_path)

def kill_vault():
    vault_path = get_vault_path()

    if vault_path.exists():
        vault_path.unlink()
    else:
        raise FileNotFoundError("Vault file does not exist")

# if __name__ == '__main__':
#     get_vault()