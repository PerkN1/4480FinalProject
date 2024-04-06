import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet

class FileEncryptor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("File Encryptor")
        self.root.geometry("500x300")  
        self.root.configure(bg='lightblue')  

        tk.Label(self.root, text="File Encryptor", font=("Helvetica", 16), bg='lightblue').pack(pady=10)

        tk.Label(self.root, text="Enter key:", bg='lightblue').pack()
        self.key_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.key_entry.pack(pady=10)

        self.generate_key_button = tk.Button(self.root, text="Generate Key", command=self.generate_key, font=("Helvetica", 12), bg='#FFFF00')  # Yellow
        self.generate_key_button.pack(pady=10)

        self.encrypt_button = tk.Button(self.root, text="Encrypt File", command=lambda: self.process_file(True), font=("Helvetica", 12), bg='#98FB98')  # Light green
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = tk.Button(self.root, text="Decrypt File", command=lambda: self.process_file(False), font=("Helvetica", 12), bg='#FFA07A')  # Light coral
        self.decrypt_button.pack(pady=10)

        self.file_path = None

    def generate_key(self):
        key = Fernet.generate_key()
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, key.decode())

    def process_file(self, encrypt=True):
        key = self.key_entry.get().encode()
        fernet = Fernet(key)
        
        if encrypt:
            action = "Encrypt"
            file_action = "encrypted"
        else:
            action = "Decrypt"
            file_action = "decrypted"
        
        input_file = filedialog.askopenfilename(title=f"Select file to {action.lower()}")
        if not input_file:
            return
        
        output_file = filedialog.asksaveasfilename(title=f"Save {file_action} file as")
        if not output_file:
            return
        
        with open(input_file, 'rb') as t:
            data = t.read()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FileEncryptor()
    app.run()