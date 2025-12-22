from platformdirs import user_data_dir
from pathlib import Path

APP_NAME = "Pawsword"

def get_app_dir():
    path = Path(user_data_dir(APP_NAME))
    path.mkdir(parents=True,exist_ok=True)
    return path

def get_vault_path():
    vault_file = get_app_dir() / "vault.enc"
    return vault_file