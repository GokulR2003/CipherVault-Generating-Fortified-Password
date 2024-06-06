import random
import string
import base64
from tkinter import *
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding as sym_padding

root = Tk()
root.geometry("1000x500")
root.configure(bg='#73b9d7')
root.title("Password Generator App") 

passwrd = StringVar()
letters_m = IntVar()
encrypt = StringVar()
text = StringVar()
decrypt = StringVar()

letters_m.set(12)
text.set("")
decrypt.set("")

def auto():
    global ans
    ans = ""
    complete_characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    for i in range(letters_m.get()):
        ans += random.choice(complete_characters)
    passwrd.set(ans)
    with open('decrypted.txt', 'w') as file1:
        file1.write(ans)

def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key

def myownhash():
    global encrypted_text
    password = ans
    key = generate_key('my_secret_password', b'salt_')
    iv = b'initial_vector12'
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    padder = sym_padding.PKCS7(128).padder()
    padded_data = padder.update(password.encode()) + padder.finalize()
    
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    encrypted_text = base64.b64encode(encrypted).decode()  # Base64 encoding
    
    with open('encrypted.txt', 'w') as file1:
        file1.write(encrypted_text)
    encrypt.set(encrypted_text)

def decrypter():
    global ascii_text
    ascii_text = ""
    encrypted_text = text.get()
    encrypted_data = base64.b64decode(encrypted_text)  # Base64 decoding
    key = generate_key('my_secret_password', b'salt_')
    iv = b'initial_vector12'
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()
    
    unpadder = sym_padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
    
    ascii_text = decrypted.decode()
    decrypt.set(ascii_text)
    with open('decrypted.txt', 'w') as file1:
        file1.write(ascii_text)

font_large = ("Segoe UI", 40, "bold")
font_medium = ("Segoe UI", 20)
font_small = ("Segoe UI", 12)

heading_label = Label(root, text="Password Generator", font=font_large, bg='#73b9d7')
heading_label.pack(pady=10)

Label(root, text="Let's craft the perfect password! How long should it be?", font=font_small, bg='#73b9d7').pack(pady=3)
Entry(root, textvariable=letters_m, font=font_small).pack(pady=3)
Button(root, text="Generate Password", font=font_small, command=auto).pack(pady=7)
Entry(root, textvariable=passwrd, font=font_small).pack(pady=3)
Button(root, text="Encrypt Password", font=font_small, command=myownhash).pack(pady=7)
Entry(root, textvariable=encrypt, font=font_small).pack(pady=3)
Label(root, text="Enter encrypted text", font=font_small, bg='#73b9d7').pack(pady=3)
Entry(root, textvariable=text, font=font_small).pack(pady=3)
Button(root, text="Decrypt Password", font=font_small, command=decrypter).pack(pady=7)
Entry(root, textvariable=decrypt, font=font_small).pack(pady=3)

root.mainloop()
