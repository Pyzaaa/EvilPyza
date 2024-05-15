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
    chunks = [message[i:i + 2000] for i in range(0, len(message), 2000)]
    return chunks

async def discorduser_mention(fetched_id):  # cleans up code from mentions and translates ID numbers into mentions
    try:
        discorduser = await bot.fetch_user(fetched_id)
        return discorduser.mention
    except discord.errors.NotFound as e:
        print(f"User to fetch not found, Error: {e}")