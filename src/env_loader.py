import os
import logging
from dotenv import load_dotenv

def load_environment_variables():
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
        logging.info(f"Environment variables loaded from {env_path}")
    else:
        logging.warning(f".env file not found at {env_path}")

def get_env_variable(key, default=None):
    value = os.getenv(key, default)
    if value is None:
        raise EnvironmentError(f"Missing required environment variable: {key}")
    return value
