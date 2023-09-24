from dotenv import load_dotenv
from os import environ

load_dotenv()
DISCORD_BOT_TOKEN = environ.get("DISCORD_BOT_TOKEN")
