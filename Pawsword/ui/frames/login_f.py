import customtkinter as ctk

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

    def login(self):
        print(f"Email: {self.email_var.get()}, Pass: {self.masterpass_var.get()}")
        self.switch_frame("vault")