import sqlite3
import discord
from discord.ext import commands
import sqlite3
from datetime import datetime, timedelta, timezone
import traceback
import sys
from aiohttp import web
import json
import random
import asyncio
import os

from utils.env_manager import EnvManager

from database.engine import engine
from database.base import Base
from database.models import WaatWord
from database.session import get_session
from database.utils import update_record

from ballboi.repository import waatword_queries


#Global Dependencies
EnvManager = EnvManager()





websockets = []  # Global list to keep track of WebSocket connections
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

#TODO: Get the entire user data, and store it in a table called users
#TODO: we will still get the current data, (for new profile pics and stuff, but will link it to a given user)
#TODO: if the only item in the message is a punctuation remove the leading space
#TODO: only retrieve the needed words from db. as we add words its going to take longer and longer
#TODO: switch to better db
#TODO: get more user information and store it in user table
#TODO: clean up code
#TODO: show the meta message in the embed
#TODO: parse words against a dictionary to find and stop common exploits like word smushing
#TODO: create mapping objects (or use an orm) so I don't have to access indices of stuff
#TODO: Settings class and settings table, this can enable things like debugs, bypasses, website, cooldown rules and times, etc
#TODO: create method for db file location (seen above)
#TODO: on meta channel slash command where you reply to a user on meta and get the words that were said around the time they made the post on the meta channel to get the context of what they were talking about (ephemeral)
#TODO: when we have all messages recorded in db, programatically create word cloud of a users words, /wordcloud 

async def construct_and_send_message(channel, message):
    waat_words = waatword_queries.get_all_waat_words()
    words_only = [word.word for word in waat_words]
    story = await join_words(words=words_only)

    last_message = waatword_queries.get_most_recent_waat_word()
    
    char_limit = 2000 # Discord's character limit
    print(f'story length{len(story)}')

    if len(story) > char_limit:
        # Truncate story from the beginning to fit within limit
        # Note: This simple truncation may cut off a word partially
        print('truncating message')
        story = '...' + story[-(char_limit-3):]
    print(f'sending a message that is {len(story)} characters long')
    await message.channel.send(story)

async def scan_channel_history(channel):
    # Assumes `channel` is a discord.TextChannel object
    # We use `oldest_first=True` to start from the beginning of the channel.
    oldest_message_id = None
    async for message in channel.history(limit=None, oldest_first=True):
        # Process each message
        # This is where you'd extract the last word and store it along with the user and timestamp.
        # For demonstration, we're just printing the message content.
        print(f"{message.author}: {message.content}")
        insert_word(str(message.author.id), message.content, message.created_at)
        oldest_message_id = message.id
    
    if oldest_message_id:
        print(f"Finished scanning. Oldest message ID: {oldest_message_id}")
    else:
        print("No messages found.")

async def find_forum_post_by_title(forum_channel_name, post_title):
    guild = bot.get_guild(EnvManager.GUILD_ID)
    if not guild:
        print("Guild not found")
        return None
    else:
        print(f"Connected to Guild: {guild.name}")
    
    # Find the forum channel by name
    
    forum_channel = discord.utils.get(guild.text_channels, name=forum_channel_name, type=discord.ChannelType.forum)
    
    if not forum_channel:
        print("Forum channel not found")
        return None
    else:
        forum_channel.send("Connected")

    # Assuming active_threads attribute or similar method is available to list threads.
    # This might need adjustment based on the discord.py version or fork you're using.
    threads = await forum_channel.threads()  # Adjust this based on the actual method to get threads
    
    for thread in threads:
        if thread.name == post_title:
            return thread  # Found the forum post (thread) by title

    return None  # No matching forum post found

@bot.event
async def on_ready():
    if EnvManager.TEST:
        print("TEST mode on, do not use in production, fr")
    
    #TODO: not working come back to later adrian
    # forum_channel_name = 'hobbies-and-misc'  
    # post_title = 'Word at a Time Story'  

    # #for cn in bot.get_all_channels():
    # #    print(cn.name)
    # thread = await find_forum_post_by_title(forum_channel_name, post_title)
    # if thread:
    #     print(f"Found forum post: {thread.name} (ID: {thread.id})")
    # else:
    #     print("Forum post not found")


    # channel = discord.utils.get(bot.get_all_channels(), name=channel_name)
    # for cn in bot.get_all_channels():
    #     print(cn.name)
    # if channel:
    #     print(f"Channel Name: {channel.Name}" )
    #     channel.send("Story Bot Online!")
    
    # else:
    #     print(f"Channel: {channel_name} not found")

    #WARN TODO NOTE debug False here
    
    # if channel and False:
    #     print("scanning channel")
    #     await scan_channel_history(channel=channel)
    #     print('scan complete')
    # else:
    #     print("chan not found")
    print(f'Logged in as {bot.user.name}')

class ButtonViews(discord.ui.View): 
    def __init__(self, *, timeout: float | None = 180, record_id):
        super().__init__(timeout=None)
        self.record_id = record_id

        full_story_button = discord.ui.Button(label="View The Full Story", style=discord.ButtonStyle.link, url='https://story.deadbolt.info')
        self.add_item(full_story_button)
        self.add_item(CapitalButton(label="A→a", record_id=record_id))

    @discord.ui.button(label="Edit", style=discord.ButtonStyle.primary, emoji="⚠")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("edit button", ephemeral=True)
    
class CapitalButton(discord.ui.Button):
    def __init__(self, label, record_id, style=discord.ButtonStyle.primary, emoji=None):
        super().__init__(label=label, style=style, custom_id=f"{label}_{record_id}", emoji=emoji)
        self.record_id = record_id

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        print(f"Record ID: {self.record_id}")
        message = waatword_queries.get_waat_word_by_id(self.record_id)
        print(f"Converting word: {message.word}")
        completion_text = ""
        try:
            new_word = message.word[0].swapcase() + message.word[1:]
            print(f"converted: {new_word}")
            update_record(model=WaatWord, record_id=self.record_id, field_name='word', new_value=new_word)
            completion_text = f"converted: {message.word}"
        except Exception as e:
            print(e)
            completion_text = f"Unable to convert {message[1]}"
        finally:
            await interaction.followup.send(completion_text, ephemeral=True)

async def join_words(words):
    words_with_spaces = ""
    punctuation = {",", ".", ":", ";", "!", "?"}
    for word in words:
        if word in punctuation:
            words_with_spaces += word
        else:
            if words_with_spaces:
                words_with_spaces += " "
            words_with_spaces += word
    return words_with_spaces

@bot.event
async def on_message(message):
    if message.author == bot.user:
        print(f"bot message: {message.content} | ignoring message")
        return

    waat_channel = discord.utils.get(bot.get_all_channels(), name=EnvManager.WAAT_CHANNEL_NAME)
    if waat_channel is None:
        print(f"waat_channel not found. Looking for {EnvManager.WAAT_CHANNEL_NAME}")
    #TODO: extract the waat_functionality out of on_message to clean up on_message

    try:
        if message.channel.name != EnvManager.WAAT_CHANNEL_NAME:
            return

        # Extract the first word from the message
        message_parts = message.content.split(maxsplit=1)  # Split the message into two parts at most
        first_word = message_parts[0] if message_parts else None  # First word is the first part
        rest_of_message = message_parts[1] if len(message_parts) > 1 else ""  # Rest of the message is the second part, if it exists

        avatar = None
        if first_word:  # Proceed if there's at least one word in the message
            author_id = message.author.id
            author_name = message.author.display_name
            timestamp = message.created_at
            if message.author.avatar:
                avatar = message.author.avatar.url
            else:
                avatar = ''

            previous_word = waatword_queries.get_most_recent_waat_word()
            if previous_word is not None: #send the starter message
                if author_name == previous_word.user and not EnvManager.TEST: # Check if this user was the last one to send a message
                    raise Exception("You were the last one to contribute to the story.")
                
                #checking that the previous message is old enough that the person read it.
                last_message_timestamp = previous_word.timestamp
                last_message_timestamp = last_message_timestamp.replace(tzinfo=timezone.utc)
                random_seconds = random.randint(3, 5)
                delta = timedelta(seconds=random_seconds)
                new_timestamp = last_message_timestamp + delta
                if new_timestamp >= datetime.now(timezone.utc): #plus a random number between 3and 5 seconds
                    raise Exception("It has been too soon since the previous message. try again in a moment")

            # Insert the word into the database

            record_id = waatword_queries.add_new_word(word=first_word, user=author_name, timestamp=timestamp, meta_message=rest_of_message, avatar_url=avatar)
            await broadcast_new_word(word=first_word, user=author_name, timestamp=timestamp, meta_message=rest_of_message, avatar=avatar)
            # After processing, construct and send the updated story
            await construct_and_send_message(channel=waat_channel, message=message)

            embed = discord.Embed(
            description=f'{first_word}' 
            )
            embed.set_footer(text=record_id)
            embed.set_thumbnail(url=avatar)
            embed.set_author(name=f"{author_name} Said:")
            await message.channel.send(embed=embed)
            await message.channel.send(view=ButtonViews(record_id=record_id))
            await message.add_reaction("✅")
            await message.delete()
            message.channel

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        # Send a message and reaction when it fails
        await message.channel.send(str(e))
        if EnvManager.TEST:
            await message.channel.send(str(traceback.format_exc()))
        await message.add_reaction("❌")

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    global websockets
    websockets.append(ws)
    try:
        async for msg in ws:
            # Handle incoming messages if necessary
            pass
    finally:
        websockets.remove(ws)

    return ws

async def broadcast_new_word(word, user, timestamp, meta_message, avatar):
    # Construct the message to send to WebSocket clients
    #message = {'word': word}
    message = {"word": word, "author": user, "timestamp": str(timestamp), "avatar_url": avatar, "meta_message": meta_message}

    dead_websockets = []
    for ws in websockets:
        try:
            await ws.send_json(message)
        except ConnectionResetError:
            dead_websockets.append(ws)
    for ws in dead_websockets:
        websockets.remove(ws)

async def handle_story(request):
    words_with_details = waatword_queries.get_all_waat_words()
    return web.json_response(words_with_details)
    # story = ' '.join(words)
    # return web.FileResponse('index.html')
    # return web.Response(text=story, content_type='text/html')

async def root_handler(request):
    raise web.HTTPFound('/static/index.html')

async def Process_Existing_story(request):
    
    
    pass

async def audit_handler(request):
    return web.FileResponse('./static/audit.html')

async def fetch_next_message(request):
    pass

async def process_response(request):
    data = await request.json()
    action = data.get('action')
    #process
    return web.json_response({"status": "success"})

async def start_web_server_and_bot():
    app = web.Application()
    app['websockets'] = [] # List to keep track of WebSocket connections
    app.router.add_get('/', root_handler)
    app.router.add_get('/audit', audit_handler)
    app.router.add_get('/audit/next', fetch_next_message)
    app.router.add_post('/audit/action', process_response)
    app.router.add_static('/static/', path='static', name='static')
    #app.router.add_get('/', handle_story)  # Existing story handler
    app.router.add_get('/story', handle_story)
    app.router.add_get('/ws', websocket_handler)  # WebSocket route
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', 8080)  # Listen on localhost:8080
    await site.start()
    print('Web server running at localhost 8080')
    await bot.start(EnvManager.DISCORD_BOT_TOKEN)

def main():

    #create db tables
    Base.metadata.create_all(bind=engine)

    #initialize_db()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_web_server_and_bot())
    
if __name__ == '__main__':
    main()