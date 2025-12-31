import customtkinter as ctk
from tkinter import messagebox
from cryptography.exceptions import InvalidTag
from Pawsword.control import load_vault, vault_exists, create_vault

class LoginFrame(ctk.CTkFrame):
    def __init__(self,master,switch_frame):
        super().__init__(master)
        self.switch_frame = switch_frame

        self.email_var = ctk.StringVar()
        self.masterpass_var = ctk.StringVar()

        ctk.CTkLabel(self,text="Email:").pack(pady=5)
        ctk.CTkEntry(self,textvariable=self.email_var).pack(pady=5)

        ctk.CTkLabel(self,text="Masterpass:").pack(pady=5)
        ctk.CTkEntry(self,textvariable=self.masterpass_var, show="*").pack(pady=5)

        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=10)
        ctk.CTkButton(self, text="Make Vault", command=self.makeVault).pack(pady=10)


        self.status_label = ctk.CTkLabel(self,text="",text_color="red")
        self.status_label.pack(pady=5)

    def show_message(self, msg, duration=2000):
        self.status_label.configure(text=msg)
        self.after(duration, lambda: self.status_label.configure(text=""))

    def makeVault(self):
        email = self.email_var.get()
        masterpass = self.masterpass_var.get()

        try:
            create_vault(email,masterpass)
            self.show_message("Vault created!")
        except FileExistsError:
            self.show_message("Vault already exists! Login instead!")


    def login(self):

        email = self.email_var.get()
        masterpass = self.masterpass_var.get()

        if not vault_exists():
            self.show_message("Vault does not exist!")
            return
        
        try:
            vault = load_vault(email,masterpass)
            vault_frame = self.master.frames["vault"]
            vault_frame.set_credentials(email,masterpass)
            self.switch_frame("vault")
        except InvalidTag:
            self.show_message("Incorrect email or master password!")