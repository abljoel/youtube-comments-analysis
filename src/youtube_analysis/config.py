import os
from dotenv import load_dotenv


# load key-value pairs from .env file located in the current directory
load_dotenv(".env")

try:
    YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"]
except:
    raise Exception("Create an .env file on the project root with the YOUTUBE_API_KEY")
