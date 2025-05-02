import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CRYPTO_PASSWORD = os.getenv("CRYPTO_PASSWORD", "senha_padrao_segura")

# Moderator Configuration
MODERATORS = [12345678, 87654321]

# Chat Configuration
MESSAGE_LIMIT = 50
MESSAGE_COOLDOWN = 60
MESSAGE_RETENTION_DAYS = 30

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin")
DB_NAME = os.getenv("DB_NAME", "furia_bot")
DB_PORT = int(os.getenv("DB_PORT", "3306")) 