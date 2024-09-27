from cryptography.fernet import Fernet
import os
import env01 as env

def key_write():
    enc_file = "key_file.txt"
    key = Fernet.generate_key()
    fernet = Fernet(key.decode('utf-8'))
#    with open(enc_file, "w") as kfile:
#        kfile.write(key.decode('utf-8'))
    env.chenge_var("enc_key", key.decode('utf-8'))

def enc_pass(password):
    key = os.getenv("enc_key")
#    enc_file = "key_file.txt"
#    with open(enc_file, "r") as kfile:
#        key = kfile.read()
    fernet = Fernet(key.rstrip())
    encMessage = fernet.encrypt(password.encode())
    return encMessage

def dec_pass(password):
#    enc_file = "key_file.txt"
#    with open(enc_file, "r") as kfile:
#        key = kfile.read()
    key = os.getenv("enc_key")
    fernet = Fernet(key.rstrip())
    decMessage = fernet.decrypt(password)
    return decMessage
