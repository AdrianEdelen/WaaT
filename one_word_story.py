from models import One_Word_Message
import datetime
import random


async def process_one_word_story_message(logger, db, message):
    # Extract the first word from the message
                
                message_parts = message.content.split(maxsplit=1)  # Split the message into two parts at most
                logger.debug("Gathered Message Parts")
                first_word = message_parts[0] if message_parts else None  # First word is the first part
                logger.debug(f"First Word in message: {first_word}")
                rest_of_message = message_parts[1] if len(message_parts) > 1 else ""  # Rest of the message is the second part, if it exists
                logger.debug(f"rest of the message (meta message): {rest_of_message}")

                avatar = None
                if first_word:  # Proceed if there's at least one word in the message
                    logger.debug("Found word in message")
                    author_id = message.author.id
                    author_name = message.author.display_name
                    timestamp = message.created_at
                    if message.author.avatar:
                        avatar = message.author.avatar.url
                    else:
                        avatar = ''
                    
                    logger.debug(f"author: {author_name}, timestamp: {timestamp}, avatar_url: {avatar}")

                    logger.debug(f"Gathering previous message from Database")
                    last_message = db.query(One_Word_Message).order_by(One_Word_Message.timestamp.desc()).first()


                    if last_message is not None: #send the starter message
                    # Check if this user was the last one to send a message
                        logger.debug(f"Previous message found in db")
                        if author_name == last_message[3] and not debug: 
                            raise Exception("You were the last one to contribute to the story.")
                        
                        #checking that the previous message is old enough that the person read it.
                        #last_message_timestamp = datetime.strptime(last_message[2], "%Y-%m-%d %H:%M:%S")
                        last_message_timestamp = datetime.fromisoformat(last_message[2])
                        random_seconds = random.randint(3, 5)
                        delta = datetime.timedelta(seconds=random_seconds)
                        new_timestamp = last_message_timestamp + delta
                        if new_timestamp >= datetime.now(datetime.timezone.utc): #plus a random number between 3and 5 seconds
                            raise Exception("It has been too soon since the previous message. try again in a moment")

                        #TODO: also add a check for the time since a given users last message. will need a users table for that



                    # Insert the word into the database
                        #TODO: this needs to be converted to the new format
                    new_word = One(word=first_word, user=author_name, timestamp=timestamp, meta_message=rest_of_message, avatar=avatar)
                    db.add(new_word)
                    db.commit()
                    #record_id = insert_word(word=first_word, user=author_name, timestamp=timestamp, meta_message=rest_of_message, avatar_url=avatar)
                    await broadcast_new_word(word=first_word, user=author_name, timestamp=timestamp, meta_message=rest_of_message, avatar=avatar)
                    # After processing, construct and send the updated story
                    await construct_and_send_message(channel=one_word_channel_name, message=message)

                    embed = discord.Embed(
                    description=f'{first_word}' 
                    )
                    embed.set_footer(text="1") #should be record id
                    embed.set_thumbnail(url=avatar)
                    embed.set_author(name=f"{author_name} Said:")
                    #await delete_last_message(message.channel)
                    await message.channel.send(embed=embed)
                    await message.channel.send(view=ButtonViews(record_id=1)) #record_id should not be temp value #TODO
                    await message.add_reaction("✅")
                    await message.delete()
                    message.channel
                    #await save_last_message(channel_id=message.channel.id, message_id=message.id)

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