import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    key_entry.delete()
    key_entry.insert(key.decode())

def process_file(encrypt=True):
    key = key_entry.get()
    encodedkey = key.encode()
    fernet = Fernet(encodedkey)
    
    action = "Encrypt" if encrypt else "Decrypt"
    file_prompt = "Select file to {}" .format(action.lower())
    
    input_file = filedialog.askopenfilename(title=file_prompt)
    if not input_file:
        return
    
    output_file = filedialog.asksaveasfilename(title="Save {}ed file as".format(action.lower()))
    if not output_file:
        return
    
    with open(input_file, 'rb') as f:
        file = f.read()
    
    if encrypt:
        processed_data = fernet.encrypt(file)
    else:
        processed_data = fernet.decrypt(file)
    
    with open(output_file, 'wb') as f:
        f.write(processed_data)
    
    result_label.config(text="File {}ed successfully!".format(action), fg="#4CAF50")

# Create the main window
root = tk.Tk()
root.title("Encryption and Decryption Tool")
root.geometry("400x250")
root.configure(bg="#424242")

# Create key entry widget with padding
key_label = tk.Label(root, text="Enter Key:", bg="#424242", fg="#EEEEEE")
key_label.grid(row=0, column=0, padx=10, pady=10)

key_entry = tk.Entry(root, bg="#616161", fg="#EEEEEE", bd=0)
key_entry.grid(row=0, column=1, padx=10, pady=10)

# Create a button to generate a random key with padding
generate_button = tk.Button(root, text="Generate Key", command=generate_key, bg="#1976D2", fg="#EEEEEE", bd=0, relief="flat")
generate_button.grid(row=0, column=2, padx=10, pady=10)

# Create buttons for encryption and decryption with padding
encrypt_button = tk.Button(root, text="Encrypt File", command=lambda: process_file(True), bg="#616161", fg="#EEEEEE", bd=0, relief="flat")
encrypt_button.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

decrypt_button = tk.Button(root, text="Decrypt File", command=lambda: process_file(False), bg="#616161", fg="#EEEEEE", bd=0, relief="flat")
decrypt_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Create a label to display results with padding
result_label = tk.Label(root, text="", bg="#424242", fg="#EEEEEE")
result_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Run the main event loop
root.mainloop()
