import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    key_entry.delete(0, tk.END)
    key_entry.insert(0, key.decode())

def process_file(encrypt=True):
    key = key_entry.get().encode()
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
    
    if encrypt:
        processed_data = fernet.encrypt(data)
    else:
        processed_data = fernet.decrypt(data)
    
    with open(output_file, 'wb') as t:
        t.write(processed_data)
    
    result_label.config(text=f"File {action.lower()}ed successfully!", fg="#4CAF50")

root = tk.Tk()
root.title("Encryption and Decryption Tool")
root.geometry("400x250")
root.configure(bg="#424242")

key_label = tk.Label(root, text="Enter Key:", bg="#424242", fg="#EEEEEE")
key_label.place(relx=0.1, rely=0.1)
key_entry = tk.Entry(root, bg="#616161", fg="#EEEEEE", bd=0)
key_entry.place(relx=0.35, rely=0.1)

generate_button = tk.Button(root, text="Generate Key", command=generate_key, bg="#1976D2", fg="#EEEEEE", bd=0, relief="flat")
generate_button.place(relx=0.65, rely=0.1)

encrypt_button = tk.Button(root, text="Encrypt File", command=lambda: process_file(True), bg="#616161", fg="#EEEEEE", bd=0, relief="flat")
encrypt_button.place(relx=0.1, rely=0.4, relwidth=0.8)
decrypt_button = tk.Button(root, text="Decrypt File", command=lambda: process_file(False), bg="#616161", fg="#EEEEEE", bd=0, relief="flat")
decrypt_button.place(relx=0.1, rely=0.6, relwidth=0.8)

result_label = tk.Label(root, text="", bg="#424242", fg="#EEEEEE")
result_label.place(relx=0.1, rely=0.8)

root.mainloop()
