

import os
import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import traceback
from aiohttp import web
import random
import asyncio

import Settings
from database import Database
import Webserver
import logging
import sys


from models import User, One_Word_Message

#TODO: This is for dev only
#TODO: setup dev env vars better
debug = True
one_word_channel_name = 'teststory'
meta_channel_name = 'teststory-meta'
guild_id = 936034644166598757
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




#how does this work?
async def delete_last_message(self, channel):
        last_message_id = self.get_last_bot_message(channel.id)
        if last_message_id:
            try:
                msg = await channel.fetch_message(last_message_id)
                await msg.delete()
            except Exception as e:
                print(f"Failed to delete message: {e}")


async def construct_and_send_message(channel, message):
    words = get_all_words()
    story = await join_words(words=words)

    last_message = get_last_message()
    
    if last_message:
        last_word_note = f"Last word added by {last_message[3]}: {last_message[1]}"  
    else:
        last_word_note = "No contributions yet!"
    if last_message[5] != "":
        last_word_note += f"\nmeta: { last_message[5]}"
    
    # Discord's character limit
    char_limit = 2000
    print(f'story length: {len(story)}')

    if len(story) > char_limit:
        # Truncate story from the beginning to fit within limit
        # Note: This simple truncation may cut off a word partially;
        print('truncating message')
        story = '...' + story[-(char_limit-3):]
    print(f'sending a message that is {len(story)} characters long')
    await message.channel.send(story)


async def scan_channel_history(channel):
    oldest_message_id = None
    async for message in channel.history(limit=None, oldest_first=True):
       
        print(f"{message.author}: {message.content}")
        insert_word(str(message.author.id), message.content, message.created_at)
        oldest_message_id = message.id
    
    if oldest_message_id:
        print(f"Finished scanning. Oldest message ID: {oldest_message_id}")
    else:
        print("No messages found.")


async def find_forum_post_by_title(forum_channel_name, post_title):
    guild = bot.get_guild(guild_id)
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
    if debug:
        print("Debug mode on, do not use in production, fr")
        

    forum_channel_name = 'hobbies-and-misc' 
    post_title = 'Word at a Time Story'  

    #TODO: why doesn't this seem to work?
    thread = await find_forum_post_by_title(forum_channel_name, post_title)
    if thread:
        print(f"Found forum post: {thread.name} (ID: {thread.id})")
    else:
        print("Forum post not found")

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
        message = get_message_by_id(self.record_id)
        print(f"Converting word: {message[1]}")
        completion_text = ""
        try:
            new_word = message[1][0].swapcase()
            print(f"converted: {new_word}")
            update_message_word(new_word, record_id=self.record_id )
            completion_text = f"converted: {message[1]}"
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
    channel = discord.utils.get(bot.get_all_channels(), name=one_word_channel_name)
    logger = logging.getLogger(__name__)
    logger.debug(f"On Message: {message.channel.name}")


    with get_db() as db:

        try:
            if message.author == bot.user:
                logger.debug("Message is made by bot exiting message processor")
                #TODO: is there anything we want to do with bot messages?
                return


            author_id = message.author.id
            user = db.query(User).filter(User.discord_user_id == author_id).first()
            if user is None:
                if message.author.avatar:
                        avatar = message.author.avatar.url
                else:
                    avatar = ''
                user = User(discord_user_id=author_id, display_name=message.author.display_name, username=message.author.name, current_avatar_url=avatar)
                db.add(user)
                db.commit()
                db.refresh(user)

            #TODO: this assumes channel_name is the one word story, we want to be more specific here
            #TODO: this handler handles every message sent to the server so it will do other stuff.
            if message.channel.name != one_word_channel_name:
                logger.debug("Message is not One Word Story")

                return
            if (message.channel.name == one_word_channel_name):
                logger.info("Message is a one word story message, processing...")
                await process_one_word_story_message(logger, db, message)
                

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            # Send a message and reaction when it fails
            await message.channel.send(str(e))
            if debug:
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

#----------------------------
# from sqlalchemy.orm import Session
# from database import SessionLocal, engine
# from models import Base, User, Word

# # Create database tables
# Base.metadata.create_all(bind=engine)

# # Start a session
# db = SessionLocal()
# db.User
# # Create a new user
# new_user = User(name='John Doe', email='john@example.com')
# db.add(new_user)
# db.commit()

# # Add a new word associated with the user
# new_word = Word(content='Hello', user_id=new_user.id)
# db.add(new_word)
# db.commit()

# # Alternatively, you can add words using the relationship
# new_user.words.append(Word(content='World'))
# db.commit()
#------------------------------
def get_db():
    database_url = os.getenv("DATABASE_URL")
    db_instance = Database.get_instance(database_url=database_url)
    return db_instance.SessionLocal()
    

async def start_services():
    
    WEBSERVER_URL = os.getenv("WEBSERVER_URL")
    WEBSERVER_PORT = os.getenv("WEBSERVER_PORT")
    web_server = Webserver.Webserver(WEBSERVER_URL, WEBSERVER_PORT)
    await web_server.start()
    print(f"Web Server Started at {web_server.host}{web_server.port}")

    DISCORD_API_KEY = os.getenv("DISCORD_API_KEY")
    await bot.start(DISCORD_API_KEY)

def main():

    #-----------------Logger Setup-----------------
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s() - %(lineno)d')
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    logger.debug("Logger Started")
    #----------------------------------------------



    #-----------------Environment Var Setup-----------------
    logger.debug("Loading Env Vars")
    Settings.load_env_specific_env()
    #-------------------------------------------------------



    #-----------------Database Setup-----------------
    # logger.debug("Initializing Database")
    # DATABASE_URL = os.getenv("DATABASE_URL")
    # db = Database(DATABASE_URL)
    # if db.init_database(DATABASE_URL):
    #     logger.info("Connected to DB")
    # else:
    #     logger.critical("Unable to connect to db")
    #     sys.exit(1)
    #------------------------------------------------
 


    #-----------------Main Loop and Start Services-----------------
    logger.debug("Starting Event Loop")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_services())
    #--------------------------------------------------------------

if __name__ == '__main__':
    main()


    # DEBUG=10.
    # INFO=20.
    # WARN=30.
    # ERROR=40.
    # CRITICAL=50.