import random
import discord
from EvilPyzaValidate import UserCheck
import subprocess
from Importedbot import bot, split_message
from EvilPyzaValidate import rcon_password  # Security
from mcrcon import MCRcon

# Minecraft Server RCON configuration
rcon_host = 'localhost'
rcon_port = 25577


@bot.command()
async def season3command(ctx, *, command):
    if await UserCheck(ctx):
        async with ctx.typing():
            # Connect to Minecraft server using RCON
            with MCRcon(rcon_host, rcon_password, port=rcon_port) as mcr:
                # Send command to Minecraft server
                response = mcr.command(command)

            # Split response into chunks if it's too long
            response_chunks = split_message(response)

            # Send each chunk separately
            for chunk in response_chunks:
                await ctx.send(chunk)
