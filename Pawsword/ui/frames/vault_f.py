import customtkinter as ctk

class VaultFrame(ctk.CTkFrame):
    def __init__(self,master,switch_frame):
        super().__init__(master)
        self.switch_frame = switch_frame

        self.email_var = ctk.StringVar()
        self.masterpass_var = ctk.StringVar()

        ctk.CTkLabel(self,text="Hello").pack(pady=5)
        ctk.CTkLabel(self,text="welcome to da vualt").pack(pady=5)


    # def login(self):
    #     print(f"Email: {self.email_var.get()}, Pass: {self.masterpass_var.get()}")
    #     self.switch_frame("vault")