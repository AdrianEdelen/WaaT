import os
class EnvManager:
    def __init__(self):
        self.DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "No Token")
        self.GUILD_ID = os.getenv("GUILD_ID", "NO GUILD ID")
        self.TEST = os.getenv("TEST", False)
        self.WEBSERVER_PORT = os.getenv("WEBSERVER_PORT", 8080)
        self.WAAT_CHANNEL_NAME = os.getenv("WAAT_CHANNEL_NAME", "Waat") 
        self.WAAT_META_CHANNEL_NAME = os.getenv("WAAT_META_CHANNEL_NAME", "Waat-meta")

    @staticmethod
    def get_env_variable(name, default=None):
        try:
            return os.environ[name]
        except KeyError:
            if default is not None:
                return default
            else:
                raise Exception(f"Environement variable {name} not set.")

