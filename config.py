from dotenv import load_dotenv
import os

load_dotenv()  # Cargar variables desde .env

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
AUTHORITY = os.getenv('AUTHORITY')
REDIRECT_PATH = os.getenv('REDIRECT_PATH')
SECRET_KEY = os.getenv('SECRET_KEY')
TELEGRAM_BOT_URL = os.getenv('TELEGRAM_BOT_URL')
SCOPE = ["User.Read"]