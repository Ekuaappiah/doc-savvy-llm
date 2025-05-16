from dotenv import load_dotenv
import os


def get_google_api_key() -> str:
    """
    Loads the environment variables and returns the Google API key.
    Raises a ValueError if the key is not found.
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment.")
    return api_key
