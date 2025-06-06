# Use the official Python image as a base
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code
COPY . .

# Set environment variable defaults if not provided
ENV DISCORD_BOT_TOKEN=YourTokenHere
ENV GUILD_ID=guildId
ENV WAAT_CHANNEL_NAME=ChannelNameHere
ENV WAAT_META_CHANNEL_NAME=MetaChannelNameHere

# Expose volume for external database storage
VOLUME /data

EXPOSE 8080

# Run the bot script when the container launches
CMD ["python", "-m", "ballboi.main"]
