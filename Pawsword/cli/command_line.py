from Pawsword.control import add_entry, get_entry, vault_exists, list_services, remove_entry
import typer
from getpass import getpass
from cryptography.exceptions import InvalidTag

app = typer.Typer()

session = {"email": None, "masterpass": None}

def login():

    if not vault_exists():
        typer.echo("Vault does not exist")
        return typer.Exit()

    typer.echo("--------------")

    session["email"] = typer.prompt("Email")
    session["masterpass"] = getpass("Masterpass: ")

    typer.echo("--------------")

def require_login():
    if not session["email"] or not session["masterpass"]:
        login()

@app.command()
def add(service: str):
    require_login()

    username = typer.prompt(f"Username for {service}")
    password = getpass(f"Password for {service}: ")

    try:
        add_entry(session["email"],session["masterpass"],service,username,password)
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
        remove_entry(session["email"],session["masterpass"],service)
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
        services = list_services(session["email"],session["masterpass"])

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