import os
from typing import Literal, Union, get_args
from dotenv import load_dotenv


required_env_keys = Literal[
    "OPENAI_API_KEY", "DYNADOK_INTERNAL_AUTH_KEY", "DYNADOK_API_BASE_URL"
]

optional_env_keys = Literal[""]

for key in get_args(required_env_keys):
    if not os.getenv(key):
        raise ValueError(f"Missing environment variable: {key}")


class AppConfig:
    @staticmethod
    def load_env():
        print(os.getcwd())
        if os.path.exists(".env"):
            load_dotenv(".env")
        else:
            load_dotenv()

    @staticmethod
    def get_env(key: Union[required_env_keys, optional_env_keys], default=None):
        value = os.getenv(key, default)
        if value == "":
            return None
        return value
