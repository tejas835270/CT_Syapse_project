import base64
from Crypto.Cipher import AES
import sys


def encrypt(msg, key):
    '''
    Purpose : This method is useful to encrypt any given text-msg using a key as a password
    :param msg: msg can be in string/encoded format which needs to be encrypted
    :param key: key is 16 digit alpha-numeric string which is used as password for encrypt
    :return: encrypted string
    '''
    # if 'byte' in type(msg):
    if msg.__class__ == bytes:
        byte_var = msg
    else:
        byte_var = msg.encode().rjust(64)
    if key.__class__ != bytes:
        key = key.encode()
    # else:
    #     byte_var = msg.encode().rjust(64)
    cipher = AES.new(key, AES.MODE_ECB)  # never use ECB in strong systems obviously
    encoded = base64.b64encode(cipher.encrypt(byte_var))
    encoded_str = encoded.decode("utf-8")
    return encoded_str.strip()


def decrypt(msg, key):
    '''
    Purpose : This method is useful to decrypt any given text-msg using a key as a password
    :param msg: msg can be in string/encoded format which needs to be decrypted
    :param key: key is 16 digit alpha-numeric string which is used as password for decrypt (it should be same which was used while encrypt)
    :return: encrypted string
    '''
    if msg.__class__ == bytes:
        byte_var = msg
    else:
        byte_var = msg.encode().rjust(64)
    if key.__class__ != bytes:
        key = key.encode()
    cipher = AES.new(key, AES.MODE_ECB)
    decoded = cipher.decrypt(base64.b64decode(byte_var))
    decoded_str = decoded.decode("utf-8")
    return decoded_str.strip()


def main():
    '''
    Purpose : This method is used to encyrpt or decrypt the string from command line
    :return: Returns the encrypted/decrypted value in string format
    example: In command line (terminal), navigate till directory for encrypt_decrypt.py and run command
    python encrypt_decrypt.py <encrypt/decrypt> <msg> <key>
    '''
    # print command line arguments
    if sys.argv[1] == 'encrypt':
        var_val = encrypt(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'decrypt':
        var_val = decrypt(sys.argv[2], sys.argv[3])
    print(var_val)

if __name__ == "__main__":
    main()
