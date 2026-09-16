import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


API_KEY = os.getenv("OPENAI_API_KEY")


if not API_KEY:
    raise ValueError(
        "OPENAI_API_KEY is missing. "
        "Please check your .env file."
    )


client = OpenAI(
    api_key=API_KEY
)