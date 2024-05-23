# This fixes user ID to ping translation for other files than EvilPyza.py, use that from now


import discord
from discord.ext import commands


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