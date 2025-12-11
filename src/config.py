import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Aviationstack API configuration
AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
BASE_URL = os.getenv("AVIATIONSTACK_BASE_URL", "https://api.aviationstack.com/v1")

