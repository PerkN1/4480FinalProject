import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet
import os

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

        self.generate_key_button = tk.Button(self.root, text="Generate Key", command=self.generate_key, font=("Helvetica", 12), bg='#FFFF00', relief=tk.FLAT)  # Yellow
        self.generate_key_button.pack(pady=10)

        self.encrypt_button = tk.Button(self.root, text="Encrypt File", command=lambda: self.process_file(True), font=("Helvetica", 12), bg='#98FB98', relief=tk.FLAT)  # Light green
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = tk.Button(self.root, text="Decrypt File", command=lambda: self.process_file(False), font=("Helvetica", 12), bg='#FFA07A', relief=tk.FLAT)  # Light coral
        self.decrypt_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", bg="lightblue", fg="#212121", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

        self.file_path = None

    def generate_key(self):
        key = Fernet.generate_key()
        self.key_entry.delete(0, tk.END)  
        self.key_entry.insert(0, key.decode())  
        self.key_entry.update_idletasks()  

    def process_file(self, encrypt=True):
        key = self.key_entry.get()
        encodedkey = key.encode()
        fernet = Fernet(encodedkey)
        
        action = "Encrypt" if encrypt else "Decrypt"
        file_prompt = "Select file to {}" .format(action.lower())
        
        input_file = filedialog.askopenfilename(title=file_prompt)
        if not input_file:
            return
        else:
            print("File successfully selected!") 
        
        print("Processing the selected file...")
        if encrypt:
            print("Encrypting the file...")
        else:
            print("Decrypting the file...")
        
        print("File processing complete!")
        
        if encrypt:
            output_file = input_file + ".encrypted" 
            key_file = os.path.join(os.path.dirname(input_file), "encryption_key.txt")
            with open(key_file, 'wb') as kf:
                kf.write(key.encode()) 
        else:
            if not input_file.endswith(".encrypted"):
                self.result_label.config(text="Cannot decrypt. File is not encrypted.", fg="red")
                return
            output_file = os.path.splitext(input_file)[0] 
            key_file = os.path.join(os.path.dirname(input_file), "encryption_key.txt")
            os.remove(key_file) 
        
        with open(input_file, 'rb') as f:
            file = f.read()
        
        if encrypt:
            processed_data = fernet.encrypt(file)
            os.remove(input_file) 
        else:
            processed_data = fernet.decrypt(file)
            os.remove(input_file) 
    
        with open(output_file, 'wb') as f:
            f.write(processed_data)
        
        if encrypt:
            self.result_label.config(text="File {}ed successfully! Saved as: {}".format(action, output_file), fg="#4CAF50")
        else:
            self.result_label.config(text="File {}ed successfully!".format(action), fg="#4CAF50")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FileEncryptor()
    app.run()
