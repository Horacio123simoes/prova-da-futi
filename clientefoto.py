import customtkinter as ctk
from tkinter import filedialog, messagebox
import socket
import threading
import os
from PIL import Image, ImageTk
import io

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class LoginScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login - Chat")
        self.geometry("600x400")
        self.resizable(False, False)

        self.left_frame = ctk.CTkFrame(self, width=300)
        self.left_frame.pack(side="left", fill="y")

        self.name_entry = ctk.CTkEntry(self.left_frame, placeholder_text="Digite seu nome")
        self.name_entry.pack(pady=20)

        self.photo_button = ctk.CTkButton(self.left_frame, text="Selecionar Foto", command=self.select_photo)
        self.photo_button.pack(pady=10)

        self.start_button = ctk.CTkButton(self.left_frame, text="Entrar no Chat", command=self.validate_login)
        self.start_button.pack(pady=20)

        self.right_frame = ctk.CTkFrame(self, width=300)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.logo_label = ctk.CTkLabel(self.right_frame, text="Try Chat", font=("Arial", 24))
        self.logo_label.pack(pady=30)

        self.photo_path = None

    def select_photo(self):
        self.photo_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg")])
        if self.photo_path:
            messagebox.showinfo("Foto", "Foto selecionada com sucesso!")

    def validate_login(self):
        name = self.name_entry.get()
        if not name or not self.photo_path:
            messagebox.showerror("Erro", "Nome e foto são obrigatórios!")
            return
        self.destroy()
        ChatApp(name, self.photo_path).mainloop()


class ChatApp(ctk.CTk):
    def __init__(self, username, photo_path):
        super().__init__()
        self.title("Chat Seguro")
        self.geometry("700x500")
        self.resizable(False, False)

        self.username = username
        self.photo_path = photo_path

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("127.0.0.1", 7000))

        # Header
        self.top_frame = ctk.CTkFrame(self, height=60)
        self.top_frame.pack(side="top", fill="x")

        img = Image.open(photo_path).resize((40, 40))
        self.profile_img = ImageTk.PhotoImage(img)
        self.img_label = ctk.CTkLabel(self.top_frame, image=self.profile_img, text="")
        self.img_label.pack(side="left", padx=10)

        self.status_label = ctk.CTkLabel(self.top_frame, text=f"{username} Online", text_color="green", font=("Arial", 16))
        self.status_label.pack(side="left")

        # Chat frame
        self.chat_frame = ctk.CTkScrollableFrame(self, fg_color="white")
        self.chat_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Bottom frame
        self.bottom_frame = ctk.CTkFrame(self, height=50)
        self.bottom_frame.pack(side="bottom", fill="x", padx=10, pady=5)

        self.msg_entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="Digite sua mensagem...")
        self.msg_entry.pack(side="left", fill="x", expand=True, padx=5)

        self.send_photo_btn = ctk.CTkButton(self.bottom_frame, text="📷", width=40, command=self.send_photo)
        self.send_photo_btn.pack(side="right", padx=5)

        self.send_button = ctk.CTkButton(self.bottom_frame, text="Enviar", command=self.send_message)
        self.send_button.pack(side="right", padx=5)

        # Thread para receber
        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()

    def display_message(self, message, sender="other"):
        bubble_color = "#d3d3d3" if sender == "other" else "#a8f0c6"
        anchor = "w" if sender == "other" else "e"

        label = ctk.CTkLabel(self.chat_frame,
                             text=message,
                             fg_color=bubble_color,
                             corner_radius=20,
                             text_color="black",
                             justify="left",
                             wraplength=300,
                             padx=10, pady=5)
        label.pack(anchor=anchor, padx=10, pady=2)

    def display_image(self, image_bytes, sender="other"):
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img.thumbnail((150, 150))
            img_tk = ImageTk.PhotoImage(img)
            label = ctk.CTkLabel(self.chat_frame, image=img_tk, text="")
            label.image = img_tk
            label.pack(anchor="e" if sender == "self" else "w", pady=4, padx=10)
        except Exception as e:
            print("Erro ao exibir imagem:", e)

    def send_message(self):
        message = self.msg_entry.get().strip()
        if message:
            full_msg = f"{self.username}:{message}"
            self.client.send(full_msg.encode("utf-8"))
            self.display_message(message, sender="self")
            self.msg_entry.delete(0, "end")

    def send_photo(self):
        path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg")])
        if path:
            try:
                with open(path, "rb") as f:
                    image_data = f.read()
                    header = f"{self.username}<img_size>{len(image_data)}".encode('utf-8').ljust(1024)
                    self.client.send(header)
                    self.client.sendall(image_data)
                    self.display_image(image_data, sender="self")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao enviar imagem: {e}")

    def receive_messages(self):
        while True:
            try:
                header = self.client.recv(1024).decode('utf-8').strip()
                if "<img_size>" in header:
                    user, size_str = header.split("<img_size>")
                    total_size = int(size_str)

                    received_data = b""
                    while len(received_data) < total_size:
                        packet = self.client.recv(min(4096, total_size - len(received_data)))
                        if not packet:
                            break
                        received_data += packet
                    self.display_image(received_data, sender="other")
                else:
                    if header.startswith(f"{self.username}:"):
                        continue
                    user, msg = header.split(":", 1)
                    self.display_message(msg.strip(), sender="other")
            except Exception as e:
                print("Erro ao receber:", e)
                break


if __name__ == "__main__":
    LoginScreen().mainloop()
