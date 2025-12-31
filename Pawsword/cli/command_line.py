from Pawsword.control import add_entry, get_entry, vault_exists, list_services, remove_entry, create_vault, delete_vault
import typer
from getpass import getpass
from cryptography.exceptions import InvalidTag
import keyring
import time

app = typer.Typer()

SESSION_TIMEOUT = 5*60 # five min in sec

user_data = {"email": None, "masterpass": None}

def require_login():
    if not user_data["email"]:
        user_data["email"] = typer.prompt("Email")

    password = keyring.get_password("godOPass", user_data["email"])
    if password:
        user_data["masterpass"] = password
    else:
        user_data["masterpass"] = getpass("Masterpass: ")
        keyring.set_password("godOPass", user_data["email"], user_data["masterpass"])
        keyring.set_password("godOPass_time", user_data["email"], str(time.time()))

    timestamp = keyring.get_password("godOPass_time", user_data["email"])

    if timestamp:
        if time.time() - float(timestamp) > SESSION_TIMEOUT:
            typer.secho('Timed out, logging out', fg=typer.colors.RED)
            logout()
            require_login()

@app.command()
def logout():
    if not user_data["email"]:
        user_data["email"] = typer.prompt("Email")

    keyring.delete_password("godOPass", user_data["email"])
    user_data["masterpass"] = None
    typer.secho("Logged out successfully.", fg=typer.colors.GREEN)

@app.command()
def init(email: str, masterpass: str): # creates vault
    try:
        create_vault(email,masterpass)
        typer.secho("Vault created!", fg=typer.colors.GREEN)
    except FileExistsError:
        typer.secho("Vault already exists, use pawpcli --help to see commands!", fg=typer.colors.RED)

@app.command()
def destroy():
    require_login()

    try:
        add_entry(user_data["email"], user_data["masterpass"], "CYA SUCKER", "GOODBYE", "DARKNESS MY OLD FRIEND")
    except InvalidTag:
        typer.secho("Incorrect login!", fg=typer.colors.RED)
        return
    except FileNotFoundError:
        typer.secho("No vault to delete :pf:", fg=typer.colors.RED)
        return

    remove_entry(user_data["email"], user_data["masterpass"], "CYA SUCKER")

    typer.secho("--------------------------------", fg=typer.colors.BRIGHT_RED)
    confirm = (typer.prompt("Are you sure you want to delete your vault (y/n)")).lower()

    if (confirm == "y"):
        delete_vault(user_data["email"], user_data["masterpass"])
        typer.secho("Vault exploded yippe", fg=typer.colors.GREEN)
    else:
        typer.secho("Wow you had mercy (did not remove vault)", fg=typer.colors.GREEN)

        



@app.command()
def add(service: str):
    require_login()

    username = typer.prompt(f"Username for {service}")
    password = getpass(f"Password for {service}: ")

    try:
        add_entry(user_data["email"],user_data["masterpass"],service,username,password)
        typer.secho(f"Added service {service}", fg=typer.colors.GREEN)
    except InvalidTag:
        typer.secho("Incorrect login!", fg=typer.colors.RED)
    except ValueError:
        typer.secho("Service already exists!", fg=typer.colors.RED)
    except Exception as e:
        typer.secho(f"Failed to add service: {e}", fg=typer.colors.RED)

@app.command()
def remove(service: str):
    require_login()

    try:
        remove_entry(user_data["email"],user_data["masterpass"],service)
        typer.secho(f"Removed service {service}", fg=typer.colors.GREEN)
    except InvalidTag:
        typer.secho("Incorrect login!", fg=typer.colors.RED)
    except ValueError:
        typer.secho("Service does not exist!", fg=typer.colors.RED)
    except Exception as e:
        typer.secho(f"Failed to remove service: {e}", fg=typer.colors.RED)

@app.command()
def list():
    require_login()

    try:
        services = list_services(user_data["email"],user_data["masterpass"])

        for i, service in enumerate(services):
            typer.secho(f"{i+1}. {service}", fg=typer.colors.CYAN)

    except InvalidTag:
        typer.secho("Incorrect login!", fg=typer.colors.RED)
    except ValueError:
        typer.secho("Service does not exist!", fg=typer.colors.RED)
    except Exception as e:
        typer.secho(f"Failed to list services: {e}", fg=typer.colors.RED)


def main():
    app()