import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet
import os

def generate_key():
    key = Fernet.generate_key()
    key_entry.delete(0, tk.END)  # Clear the key entry widget
    key_entry.insert(0, key.decode())  # Insert the generated key into the key entry widget

def process_file(encrypt=True):
    key = key_entry.get()
    encodedkey = key.encode()
    fernet = Fernet(encodedkey)
    
    action = "Encrypt" if encrypt else "Decrypt"
    file_prompt = "Select file to {}" .format(action.lower())
    
    input_file = filedialog.askopenfilename(title=file_prompt)
    if not input_file:
        return
    
    if encrypt:
        output_file = input_file + ".encrypted" #Adds .encryted for the encrypted file
        key_file = os.path.join(os.path.dirname(input_file), "encryption_key.txt")
        with open(key_file, 'wb') as kf:
            kf.write(key.encode()) #Writes key into text file
    else:
        if not input_file.endswith(".encrypted"):
            result_label.config(text="Cannot decrypt. File is not encrypted.", fg="red")
            return
        output_file = os.path.splitext(input_file)[0] #Removes encryption extension after decryption
        key_file = os.path.join(os.path.dirname(input_file), "encryption_key.txt")
        os.remove(key_file) #Removes key file after decryption
    
    with open(input_file, 'rb') as f:
        file = f.read()
    
    if encrypt:
        processed_data = fernet.encrypt(file)
        os.remove(input_file) #Removes input file
    else:
        processed_data = fernet.decrypt(file)
        os.remove(input_file) #removes encrypted file

    with open(output_file, 'wb') as f:
        f.write(processed_data)
    
    if encrypt:
        result_label.config(text="File {}ed successfully! Saved as: {}".format(action, output_file), fg="#4CAF50")
    else:
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
