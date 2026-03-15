from dotenv import load_dotenv
import os

load_dotenv()

FMCSA_API_KEY = os.getenv("FMCSA_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
APP_API_KEY = os.getenv("APP_API_KEY")