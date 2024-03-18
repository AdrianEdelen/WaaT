

import sqlite3
import discord
from discord.ext import commands
import sqlite3
from datetime import datetime
import traceback
import sys
from aiohttp import web
import json

import asyncio
channel_name = 'Word at a Time Story'
guild_id = 936034644166598757
db = 'live.db'
websockets = []  # Global list to keep track of WebSocket connections
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

#TODO: Get the entire user data, and store it in a table called users
#TODO: we will still get the current data, (for new profile pics and stuff, but will link it to a given user)




def initialize_db():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS story (
            id INTEGER PRIMARY KEY,
            word TEXT,
            timestamp DATETIME,
            user TEXT,
            createdOn DATETIME,
            meta_message TEST,
            avatar_url
        )
    ''')
    conn.commit()
    conn.close()




def insert_word(word, user, timestamp, meta_message, avatar_url):

    conn = sqlite3.connect(db)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO story (word, timestamp, user, createdOn, meta_message, avatar_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (word, timestamp, user, datetime.now(), meta_message, avatar_url))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f'entry already exists:{word} {timestamp} {user}')
        pass
    finally:
        conn.close()

last_author = None  # Keep track of the last author who sent a message





def get_last_message():
    """Fetch all words from the database, ordered by their position in the story."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM story ORDER BY id DESC LIMIT 1')
    last_message = cursor.fetchone()
    conn.close()
    if last_message is None:
        return None  # Handling case where there are no entries
    return last_message  # Assuming each row contains a single word in the first column.

def get_all_words():
    """Fetch all words from the database, ordered by their position in the story."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('SELECT word FROM story ORDER BY id ASC')
    words = cursor.fetchall()
    conn.close()
    return [word[0] for word in words]  # Assuming each row contains a single word in the first column.

def get_all_words_detailed():
    """Fetch all words with details from the database, ordered by their position in the story."""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    # Assuming 'user' contains the author name, and 'timestamp' is when the word was added
    cursor.execute('SELECT word, user, timestamp, meta_message FROM story ORDER BY id ASC')
    words_detailed = cursor.fetchall()
    conn.close()
    # Create a list of dictionaries, each containing the word and its details
    words_with_details = [
        {"word": word, "author": user, "timestamp": timestamp, "meta_message": meta_message}
        for word, user, timestamp, meta_message in words_detailed
    ]
    return words_with_details

async def construct_and_send_message(channel, message):
    website_url = "https://story.deadbolt.info"
    
    
    words = get_all_words()
    story = ' '.join(words)

    last_message = get_last_message()
    
    if last_message:
        last_word_note = f"Last word added by {last_message[3]}: {last_message[1]}"  # Adjusted to fetch the correct indices
    else:
        last_word_note = "No contributions yet!"
    if last_message[5] != "":
        last_word_note += f"\nmeta: { last_message[5]}"
    
    # Discord's character limit
    char_limit = 2000
    print(f'story length{len(story)}')
    final_message = f"{story}\n\n{last_word_note}"
    print(f'final message length {len(final_message)}')

    if len(final_message) > char_limit:
        # Truncate story from the beginning to fit within limit
        # Note: This simple truncation may cut off a word partially; you may need more logic for cleanly cutting off.
        print('truncating message')
        final_message = '...' + final_message[-(char_limit-3):]
    print(f'sending a message that is {len(final_message)} characters long')
    await message.channel.send(final_message)


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

    forum_channel_name = 'hobbies-and-misc'  # Replace with your forum channel's name
    post_title = 'Word at a Time Story'  # The title of the forum post you're looking for

    #for cn in bot.get_all_channels():
    #    print(cn.name)
    thread = await find_forum_post_by_title(forum_channel_name, post_title)
    if thread:
        print(f"Found forum post: {thread.name} (ID: {thread.id})")
    else:
        print("Forum post not found")


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


class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="View The Full Story", style=discord.ButtonStyle.primary, emoji="🧾") # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("View the full story at: https://story.deadbolt.info", ephemeral=True)


@bot.event
async def on_message(message):
    channel = discord.utils.get(bot.get_all_channels(), name=channel_name)

    try:
        if message.author == bot.user or message.channel.name != channel_name:
            return

        # Extract the first word from the message
        message_parts = message.content.split(maxsplit=1)  # Split the message into two parts at most
        first_word = message_parts[0] if message_parts else None  # First word is the first part
        rest_of_message = message_parts[1] if len(message_parts) > 1 else ""  # Rest of the message is the second part, if it exists

        if first_word:  # Proceed if there's at least one word in the message
            author_id = message.author.id
            author_name = message.author.display_name
            timestamp = message.created_at
            avatar = message.author.avatar.url

            last_message = get_last_message()
            if last_message is not None: #send the starter message
            # Check if this user was the last one to send a message
                if author_name == last_message[3]: 
                    raise Exception("You were the last one to contribute to the story.")
                    pass
            

            # Insert the word into the database
            insert_word(word=first_word, user=author_name, timestamp=timestamp, meta_message=rest_of_message, avatar_url=avatar)
            await broadcast_new_word(word=first_word, user=author_name, timestamp=timestamp, meta_message=rest_of_message, avatar=avatar)
            # After processing, construct and send the updated story
            await construct_and_send_message(channel=channel, message=message)
            await message.channel.send(view=MyView())
            # Add a reaction to indicate successful processing
            await message.add_reaction("✅")

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        # Send a message and reaction when it fails
        await message.channel.send(str(e))
        #await message.channel.send(str(traceback.format_exc()))
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
    message = {"word": word, "author": user, "timestamp": str(timestamp), "avatar": avatar, "meta": meta_message}

    dead_websockets = []
    for ws in websockets:
        try:
            await ws.send_json(message)
        except ConnectionResetError:
            dead_websockets.append(ws)
    for ws in dead_websockets:
        websockets.remove(ws)

async def handle_story(request):
    words_with_details = get_all_words_detailed()
    return web.json_response(words_with_details)
    story = ' '.join(words)
    return web.FileResponse('index.html')
    return web.Response(text=story, content_type='text/html')

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
    site = web.TCPSite(runner, 'localhost', 8080)  # Listen on localhost:8080
    await site.start()
    print('Web server running at localhost 8080')
    await bot.start('MTA4NTI2MjMzMDgxNzk0OTY5Ng.GlNGkW.e2B70gVpXuLh4TRYtjs1AbVvJ0ke5OBaaELf_E')

def main():
    initialize_db()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_web_server_and_bot())
    



if __name__ == '__main__':
    main()