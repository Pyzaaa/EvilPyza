# This fixes user ID to ping translation for other files than EvilPyza.py, use that from now


import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.reactions = True
intents.members = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)