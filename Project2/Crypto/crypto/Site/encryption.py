import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def encrypt_AES(key, filecontent, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(filecontent, AES.block_size))
    return encrypted_data


def decrypt_AES(key, ciphertext, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    tmp = cipher.decrypt(ciphertext)
    decrypted_data = unpad(tmp, AES.block_size)
    return decrypted_data


def encrypt(publicKey, file):
    fileContent = file.read()
    key = get_random_bytes(16)
    iv = get_random_bytes(16)
    encrypted_file = encrypt_AES(key, fileContent, iv)
    keyPub = RSA.import_key(publicKey)
    cipher = PKCS1_OAEP.new(key=keyPub)
    encrypted_key = cipher.encrypt(key)
    return encrypted_file, encrypted_key, iv


def decrypt(encryptedKey, privateKey, ciphertext, iv):
    keyPri = RSA.import_key(privateKey)
    cipher = PKCS1_OAEP.new(key=keyPri)
    decrypted_key = cipher.decrypt(base64.b64decode(encryptedKey))
    decrypted_data = decrypt_AES(decrypted_key, ciphertext, iv)
    return decrypted_data
