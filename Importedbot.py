# This fixes user ID to ping translation for other files than EvilPyza.py, use that from now


import discord
from discord.ext import commands
import logging
from logging.handlers import TimedRotatingFileHandler
import os


intents = discord.Intents.default()
intents.reactions = True
intents.members = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)


# Function to split long messages into chunks
def split_message(message):
    # Split the message by newline characters
    lines = message.split('\n')

    # Initialize variables to store the current chunk and the result
    current_chunk = ''
    chunks = []

    for line in lines:
        # Check if adding this line would exceed the limit
        if len(current_chunk) + len(line) + 1 > 2000:  # +1 for the newline character
            # If it would, append the current chunk to the result and start a new chunk
            chunks.append(current_chunk)
            current_chunk = line
        else:
            # If not, add the line to the current chunk
            if current_chunk:
                current_chunk += '\n' + line
            else:
                current_chunk = line

    # Add the last chunk to the result
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


async def discorduser_mention(fetched_id):  # cleans up code from mentions and translates ID numbers into mentions
    try:
        discorduser = await bot.fetch_user(fetched_id)
        return discorduser.mention
    except discord.errors.NotFound as e:
        print(f"User to fetch not found, Error: {e}")



# basic Logging

class ExcludeKeywordsFilter(logging.Filter):
    def __init__(self, keywords):
        super().__init__()
        self.keywords = keywords

    def filter(self, record):
        return not any(keyword in record.getMessage() for keyword in self.keywords)

# Create a logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Create a TimedRotatingFileHandler
handler = TimedRotatingFileHandler(
    filename='logs/discord_bot.log',  # Base filename
    when='midnight',  # Rotate at midnight
    interval=1,  # Rotate every day
    backupCount=0  # Keep 30 days of logs
)
handler.suffix = "%Y-%m-%d"  # Date format for rotated files

# Set the logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Set logging level

# Add the handler to the logger
logger.addHandler(handler)

# Define the keywords you want to exclude from logging
keywords_to_exclude = [
    'Got a request to RESUME the websocket',
    'Shard ID None has sent the RESUME payload',
    'Shard ID'
]

# Create the filter
exclude_filter = ExcludeKeywordsFilter(keywords_to_exclude)

# Add the filter to the handler
handler.addFilter(exclude_filter)

# Test the logging setup
logger.info('This is a test message.')
logger.info('Got a request to RESUME the websocket')  # This should be excluded
