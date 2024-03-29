import logging
import requests
import json
import asyncio

class DiscordLogger(logging.Handler):
    def __init__(self, bot, channel_id):
        super().__init__()
        self.bot = bot
        self.channel_id = channel_id

    def emit(self, record):
        log_entry = self.format(record)
        asyncio.run_coroutine_threadsafe(self.send_log_message(log_entry))

    async def send_log_message(self, message):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            await channel.send(message)