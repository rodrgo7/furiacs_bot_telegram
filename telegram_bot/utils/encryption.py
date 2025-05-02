from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from config.settings import CRYPTO_PASSWORD

class MessageEncryptor:
    def __init__(self, password: str):
        password_bytes = password.encode()
        salt = b'salt_aleatorio_'  
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        self.cipher = Fernet(key)
    
    def encrypt(self, message: str) -> str:
        """Encrypt a message string."""
        return self.cipher.encrypt(message.encode()).decode()
    
    def decrypt(self, encrypted_message: str) -> str:
        """Decrypt an encrypted message string."""
        return self.cipher.decrypt(encrypted_message.encode()).decode()

encryptor = MessageEncryptor(CRYPTO_PASSWORD) 