import sys
import time
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64, os


HELP_TEXT:str = \
"""
Usage:

python crypt.py [ACTION] [INPUT FILE PATH] [OUTPUT FILE PATH]
"""


def _key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt_file(infile, outfile, password):
    salt = os.urandom(16)
    cipher = Fernet(_key(password, salt))
    data = open(infile, "rb").read()
    encrypted = cipher.encrypt(data)
    open(outfile, "wb").write(salt + encrypted)


def decrypt_file(infile, outfile, password):
    blob = open(infile, "rb").read()
    salt, encrypted = blob[:16], blob[16:]
    cipher = Fernet(_key(password, salt))
    data = cipher.decrypt(encrypted)
    open(outfile, "wb").write(data)


def check_args(args: list[str]) -> bool:
    if args[0] in ("--help", "-h"):
        return False
    if not (args[0] in ("encrypt", "decrypt")):
        print("Bad action.")
        return False
    if not Path(args[1]).exists():
        print(f"{args[1]}: file not found")
        return False
    return True


def main():

    args = sys.argv[1:]

    if not check_args(args):
        print(HELP_TEXT)
        return

    action: str = args[0]
    input_file: str = args[1]
    output_file: str = args[2]

    if action == "encrypt":
        password = input("Enter a password to encrypt by:")
        encrypt_file(input_file, output_file, password)
        return

    if action == "decrypt":
        password = input("Enter the decryption password:")

        try:
            decrypt_file(input_file, output_file, password)
        except InvalidToken as e:
            time.sleep(3)
            print("Wrong password.")
            return
        return


if __name__ == "__main__":
    main()
