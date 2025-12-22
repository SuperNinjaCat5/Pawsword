import customtkinter as ctk
from frames.login_f import LoginFrame
from frames.vault_f import VaultFrame

ctk.set_appearance_mode("dark")

app = ctk.CTk()

app.geometry('900x700')

app.title('Pawsword')

all_frames = {}

def show_frame(f):
    for frame in all_frames.values():
        frame.pack_forget()
    all_frames[f].pack(fill="both", expand=True)

all_frames["login"] = LoginFrame(app,show_frame)
all_frames["vault"] = VaultFrame(app,show_frame)

show_frame("login")

if __name__ == '__main__':
    app.mainloop()