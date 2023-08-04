from dataclasses import dataclass
import os
from dotenv import load_dotenv


load_dotenv()


@dataclass
class MemphisCredentials:
    HOST = os.getenv("HOSTNAME")
    USERNAME = os.getenv("CLIENT_USERNAME")
    PASSWORD = os.getenv("CLIENT_PASSWORD")
    ACCOUNT_ID = os.getenv("ACCOUNT_ID")
