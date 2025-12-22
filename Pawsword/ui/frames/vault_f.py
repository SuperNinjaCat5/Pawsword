import customtkinter as ctk
from Pawsword.control import load_vault, add_entry, remove_entry, get_entry, list_services, save_vault
from cryptography.exceptions import InvalidTag

class VaultFrame(ctk.CTkFrame):
    def __init__(self,master,switch_frame):
        super().__init__(master)
        self.switch_frame = switch_frame

        ctk.CTkLabel(self,text="Vault",font=("Arial",20)).pack(pady=5)

        self.scroll_frame = ctk.CTkScrollableFrame(self,width=400,height=300)
        self.scroll_frame.pack(pady=10)

        self.service_var = ctk.StringVar()
        self.username_var = ctk.StringVar()
        self.password_var = ctk.StringVar()

        ctk.CTkLabel(self,text="Service:").pack(pady=2)
        ctk.CTkEntry(self,textvariable=self.service_var).pack(pady=2)

        ctk.CTkLabel(self,text="Username:").pack(pady=2)
        ctk.CTkEntry(self,textvariable=self.username_var).pack(pady=2)

        ctk.CTkLabel(self,text="Password:").pack(pady=2)
        ctk.CTkEntry(self,textvariable=self.password_var).pack(pady=2)

        ctk.CTkButton(self, text="Add Entry", command=self.add_entry_ui).pack(pady=5)
        ctk.CTkButton(self, text="Logout", command=lambda: self.switch_frame("login")).pack(pady=5)

        self.status_label = ctk.CTkLabel(self,text="",text_color="red")
        self.status_label.pack(pady=5)

        self.set_credentials("email@example.com","masterpass6")
        self.refresh_services()


    def set_credentials(self, email, masterpass):
        self.email = email
        self.masterpass = masterpass
        self.refresh_services()

    def show_message(self, message, duration=2000):
        self.status_label.configure(text=message)
        self.after(duration, lambda: self.status_label.configure(text=""))

    # def view_entry_ui(self, service):
    #     try:
    #         entry = get_entry(self.email, self.masterpass, service)

    #         if hasattr(self, 'view_label') and self.view_label.winfo_exists():
    #             self.view_label.destroy()

    #         self.view_label = ctk.CTkLabel(self, text=f"{service}: {entry['username']} / {entry['password']}",
    #                                         text_color="white")
    #         self.view_label.pack(pady=5)

    #         self.after(4000, lambda: self.view_label.destroy())

    #     except Exception as e:
    #         self.show_message(str(e))

    def remove_entry_ui(self, service):
        try:
            remove_entry(self.email, self.masterpass, service)
            self.show_message(f"Removed {service}")
            self.refresh_services()
        except Exception as e:
            self.show_message(str(e))

    def refresh_services(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        try:
            services = list_services(self.email, self.masterpass)

            header = ctk.CTkFrame(self.scroll_frame)
            header.pack(fill="x", pady=2, padx=5)
            for i in range(4):
                header.grid_columnconfigure(i, weight=1)

            ctk.CTkLabel(header, text="Service").grid(row=0, column=0, sticky="w", padx=5)
            ctk.CTkLabel(header, text="Username").grid(row=0, column=1, sticky="w", padx=5)
            ctk.CTkLabel(header, text="Password").grid(row=0, column=2, sticky="w", padx=5)
            ctk.CTkLabel(header, text="Remove").grid(row=0, column=3, padx=5)

            for service in services:
                entry = get_entry(self.email, self.masterpass, service)
                row_frame = ctk.CTkFrame(self.scroll_frame)
                row_frame.pack(fill="x", pady=2, padx=5)
                for i in range(4):
                    row_frame.grid_columnconfigure(i, weight=1)

                ctk.CTkLabel(row_frame, text=service, anchor="w").grid(row=0, column=0, sticky="w", padx=5)
                ctk.CTkLabel(row_frame, text=entry["username"], anchor="w").grid(row=0, column=1, sticky="w", padx=5)
                ctk.CTkLabel(row_frame, text=entry["password"], anchor="w").grid(row=0, column=2, sticky="w", padx=5)

                ctk.CTkButton(row_frame, text="Remove", width=60,
                            command=lambda s=service: self.remove_entry_ui(s)).grid(row=0, column=3, padx=5)

        except Exception as e:
            self.show_message(str(e))


    def add_entry_ui(self):
        service = self.service_var.get()
        username = self.username_var.get()
        password = self.password_var.get()

        if not service or not username or not password:
            self.show_message("All fields required!")
            return

        try:
            add_entry(self.email, self.masterpass, service, username, password)
            self.refresh_services()
        except ValueError as e:
            self.show_message(str(e))