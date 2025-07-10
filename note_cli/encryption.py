
import base64
import os
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SALT_SIZE = 16

def get_key_from_password(password: str, salt: bytes) -> bytes:
    """Derive a cryptographic key from a password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def generate_salt() -> bytes:
    """Generate a new random salt."""
    return os.urandom(SALT_SIZE)

class Encryptor:
    def __init__(self, password: str):
        """Initialize the Encryptor with a password."""
        self.password = password

    def encrypt(self, plaintext: str) -> bytes:
        """Encrypt a plaintext string. The salt is prepended to the ciphertext."""
        if not plaintext:
            return b''
        salt = generate_salt()
        key = get_key_from_password(self.password, salt)
        f = Fernet(key)
        encrypted_data = f.encrypt(plaintext.encode())
        return salt + encrypted_data

    def decrypt(self, ciphertext: bytes) -> str:
        """Decrypt a ciphertext string. The salt is expected to be prepended."""
        if not ciphertext:
            return ""
        try:
            salt = ciphertext[:SALT_SIZE]
            token = ciphertext[SALT_SIZE:]
            key = get_key_from_password(self.password, salt)
            f = Fernet(key)
            decrypted_data = f.decrypt(token)
            return decrypted_data.decode()
        except InvalidToken:
            # This can happen if the password is wrong
            raise ValueError("Decryption failed. Invalid password or corrupted data.")
        except Exception as e:
            raise ValueError(f"An unexpected error occurred during decryption: {e}") 
