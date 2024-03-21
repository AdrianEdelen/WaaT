import json
import os
import logging

def running_in_docker():
    logger = logging.getLogger(__name__)

    docker_var = "IN_DOCKER"
    true_text = "true"
    
    logger.debug(f"Checking {docker_var} for {true_text}")
    if os.getenv(docker_var) == true_text:
        logger.debug(f"{docker_var} = True")
        return True
    else:
        logger.debug(f"{docker_var} is not True") 
        return False


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