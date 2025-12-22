import customtkinter as ctk
from Pawsword.control import load_vault, add_entry, remove_entry, get_entry, list_services, save_vault
from cryptography.exceptions import InvalidTag

class VaultFrame(ctk.CTkFrame):
    def __init__(self,master,switch_frame):
        super().__init__(master)
        self.switch_frame = switch_frame

        self.email_var = ctk.StringVar()
        self.masterpass_var = ctk.StringVar()
        self.service_var = ctk.StringVar()
        self.username_var = ctk.StringVar()
        self.password_var = ctk.StringVar()

        ctk.CTkLabel(self,text="Vault",font=("Arial",20)).pack(pady=5)
        
        # self.service_listbox = ctk.CTkListbox(self, height=10, width=40)
        # self.service_listbox.pack(pady=5)
        
        # ctk.CTkLabel(self,text="Service:").pack(pady=2)
        # ctk.CTkEntry(self,textvariable=self.service_var).pack(pady=2)
        
        # ctk.CTkLabel(self,text="Username:").pack(pady=2)
        # ctk.CTkEntry(self,textvariable=self.service_var).pack(pady=2)

        # ctk.CTkLabel(self,text="Password:").pack(pady=2)
        # ctk.CTkEntry(self,textvariable=self.service_var).pack(pady=2)