import json
import os
import logging
import dotenv
import sys

def load_env_specific_env():
    try:
        logger = logging.getLogger(__name__)
        environment = os.getenv('ENVIRONMENT', 'development').lower()
        logger.debug(f"Environment is {environment}")
        if environment == "docker":
            logger.debug(f"Environment '{environment}' nothing else to do with dotenv ")
            return
        dotenv_path = f'.env.{environment}'
        logging.debug(f"dotenv_path = {dotenv_path}")
        if os.path.isfile(dotenv_path):
            result = dotenv.load_dotenv(dotenv_path=dotenv_path)
            logger.debug(f"Attempted to load env variables from .env file. Result: {result}")
            if not result:
                raise EnvironmentError
        else:
            dotenv.load_dotenv()
    except Exception as e:
        logger.exception("Failed to properly load environment variables, stuff won't work")
        sys.exit(1)



class Settings:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.load_settings_from_json()

    def load_settings_from_json(self):
        with open('settings.json', 'r') as settings_file:
            settings = json.load(settings_file)
        for key, value in settings.items():
            if isinstance(value, dict):
                value = SettingGroup(value)
            setattr(self, key, value)


class SettingGroup:
    def __init__(self, settings) -> None:
        for key, value in settings.items():
            setattr(self, key, value)