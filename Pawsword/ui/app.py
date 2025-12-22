import customtkinter as ctk
from Pawsword.control import load_vault, vault_exists
from Pawsword.ui.frames.login_f import LoginFrame
from Pawsword.ui.frames.vault_f import VaultFrame


app = ctk.CTk()

app.geometry('900x700')

app.title('Pawsword')

app.frames = {}

def show_frame(f):
    for frame in app.frames.values():
        frame.pack_forget()
    app.frames[f].pack(fill="both", expand=True)

app.frames["login"] = LoginFrame(app,show_frame)
app.frames["vault"] = VaultFrame(app,show_frame)

show_frame("login")

if __name__ == '__main__':
    app.mainloop()