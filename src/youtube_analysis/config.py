"""
API Key Configuration Module

This module loads key-value pairs from a '.env' file located in the current directory,
specifically retrieving the YouTube API key.

Functions:
    - load_dotenv: Loads key-value pairs from a '.env' file.

Variables:
    - YOUTUBE_API_KEY (str): YouTube API key loaded from the environment variables.

Raises:
    - Exception: Raised if the '.env' file is not found or does not contain the required 
      YouTube API key.

Note:
    To use this module, ensure you have a '.env' file in the project root with the YouTube API key.
"""
import os
from dotenv import load_dotenv


# load key-value pairs from .env file located in the current directory
load_dotenv(".env")

try:
    YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"]
except:
    raise Exception("Create an .env file on the project root with the YOUTUBE_API_KEY")
