from dotenv import load_dotenv
import os
from pathlib import Path
from config.util import Environment
from logger import logger

""""load environment variables"""

# # Eliminar variables de entorno antiguas si existen
for key in list(os.environ.keys()):
    os.environ.pop(key, None)

# Load env variables from a file, if exists else default would be set
logger.info("SERVER_INIT::Setting environment variables from .env file(if exists)...")
load_dotenv(
    verbose=True, dotenv_path=os.path.join(Path(__file__).parent.parent.parent, ".env")
)


class DB:
    host = Environment.get_string("DB_HOST", "localhost")
    port = Environment.get_string("DB_PORT", "5432")
    name = Environment.get_string("DB_NAME", "autoapp")
    user = Environment.get_string("DB_USER", "autoapp")
    pass_ = Environment.get_string("DB_PASS", "autoapp")


class JWTToken:
    algorithm = Environment.get_string("JWT_ALGORITHM", "HS256")
    secret = Environment.get_string("JWT_SECRET", "secret")
    access_token_expire_minutes = Environment.get_string(
        "JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"
    )
