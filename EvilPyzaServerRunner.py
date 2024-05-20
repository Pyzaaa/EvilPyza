import random
import discord
from EvilPyzaValidate import UserCheck
import subprocess
from Importedbot import bot, split_message, discorduser_mention
from EvilPyzaValidate import rcon_password  # Security
from mcrcon import MCRcon
from Economy import users, eco
import pickle

# Minecraft Server RCON configuration
rcon_host = 'localhost'
rcon_port = 25577
mcr = MCRcon(rcon_host, rcon_password, port=rcon_port)
try:
    mcr.connect()
except Exception as e:
    print(f"mcr failed to connect {e}")

Playerlist = {}

FILE_PATH = "data/minecraftplayerslist.pkl"


def saveplayers():
    with open(FILE_PATH, 'wb') as f:
        pickle.dump(Playerlist, f)


def loadplayers():
    try:
        with open(FILE_PATH, 'rb') as f:
            global Playerlist
            Playerlist = pickle.load(f)
    except EOFError:
        print("EOF Error")


loadplayers()

item_prices = {
    "oak_log": 3,
    "spruce_log": 3,
    "birch_log": 3,
    "acacia_log": 3,
    "jungle_log": 5,
    "dark_oak_log": 5,
    "granite": 3,
    "andesite": 3,
    "diorite": 3,
    "deepslate": 4,
    "sandstone": 6,
    "prismarine": 10,
    "amethyst_block": 10,
    "calcite": 10,
    "terracotta": 6,
    "slime_ball": 15,
    "cherry_log": 8,
    "cobblestone": 1,
    "dirt": 2,
    "sand": 2,
    "clay": 8,
    "mushroom_stem": 12,
    "grass_block": 6,
    "coal": 6,
    "quartz": 15,
    "iron_ingot": 20,
    "redstone": 10,
    "gold_ingot": 30,
    "lapis_lazuli": 20,
    "diamond": 100,
    "emerald": 50,
    "stone_bricks": 5,
    "glass_block": 5,
    "obsidian": 50,
    "glowstone": 15,
    "iron_sword": 25,
    "iron_pickaxe": 35,
    "diamond_pickaxe": 150,
    "diamond_sword": 150,
    "bow": 20,
    "arrow": 2,
    "iron_helmet": 40,
    "iron_chestplate": 70,
    "iron_leggings": 60,
    "iron_boots": 40,
    "diamond_helmet": 300,
    "diamond_chestplate": 600,
    "diamond_leggings": 500,
    "diamond_boots": 250,
    "white_wool": 8,
    "leather": 8,
    "gunpowder": 8,
    "bone": 5,
    "bread": 3,
    "apple": 20,
    "cooked_steak": 6,
    "golden_apple": 500,
    "candle": 5,
    "painting": 10
}
sell_prices = {
    "obsidian": 1,
    "emerald": 5,
    "diamond": 15,
    "netherite_ingot": 100,
    "nether_star": 120,
    "beacon": 130,
    "creeper_head": 50,
    "zombie_head": 30,
    "skeleton_skull": 30,
    "wither_skeleton_skull": 30,
    "dragon_head": 10,
    "elytra": 100,
    "netherite_upgrade_smithing_template": 20,
    "golden_apple": 30,
    "enchanted_golden_apple": 300
}

potion_effects = {
"fire_resistance": 200,
"strength": 200,
"invisibility": 200
}

############## /commands don't work on bukkit cause why not LMAO
@bot.command()
async def season3(ctx, command="", arg2=None, arg3=1):
    try:
        mcr.command("tick query")
        print("mcr connected")
    except Exception as e:
        print(f"mcr not connected {e}")
        await ctx.reply("Connection error, attempting reconnect...")
        try:
            mcr.connect()
        except Exception as e:
            print(f"mcr failed to connect {e}")
            await ctx.send("Connection error, server offline??")
            return
        return
    user_id = ctx.author.id
    if command == "":
        await ctx.reply("No argument provided, use `!season3 register <minecraft nickname>` to register playername or `!season3 buy <item_id> [amount=1]` to buy items")
        return
    if command == "register":
        if user_id not in Playerlist:
            if not arg2:
                await ctx.reply(f"No minecraft player name provided")
                return
            elif arg2 not in Playerlist.values():
                await eco(ctx, "add")
                Playerlist.update({user_id: arg2})
                saveplayers()
                await ctx.reply(f"Registered player {await discorduser_mention(user_id)} as {arg2}")
                return
            elif arg2 in Playerlist.values():
                await ctx.reply(f"Player nickname {arg2} already registered")
                return
            else:
                await ctx.reply(f"Unknown error")
                return
        else:
            await ctx.reply(f"Player {await discorduser_mention(user_id)} already registered as {Playerlist[user_id]}, use `!season3 unregister` to remove")
            return
    elif command == "unregister":
        if user_id in Playerlist:
            removed = Playerlist.pop(user_id)
            saveplayers()
            await ctx.reply(f"Player {await discorduser_mention(user_id)}: {removed} unregistered")
            return
        else:
            await ctx.reply("Player not found in registered players list")
            return
    elif command == "price":
        returned = ""
        if arg2 and arg2 in item_prices.keys():
            # return item price instead of whole list
            returned = f"{arg2} costs: {item_prices[arg2]}/per item\n"
        if arg2 and arg2 in sell_prices.keys():
            returned += f"{arg2} sells for: {sell_prices[arg2]}/per item"
            await ctx.reply(returned)
            return
        elif arg2:
            await ctx.reply(returned)
            return
        shop = "***EvilPyza item shop:***\n"
        for item, price in item_prices.items():
            shop += f"**{item}**: price **{price}**/per item\n"
        shop += "\n ***SELL PRICES***:"
        for item, price in sell_prices.items():
            shop += f"**{item}**: sell value **{price}**/per item\n"
        # Split response into chunks if it's too long
        response_chunks = split_message(shop)
        # Send each chunk separately
        for chunk in response_chunks:
            await ctx.send(chunk)
        return
    if command not in ["buy", "sell"]:
        await ctx.reply(f"Unknown command {command}")
        return
    elif user_id in Playerlist:
        player_name = Playerlist[user_id]
        if isinstance(arg3, str) or arg3 < 1:
            arg3 = 1
        if is_player_online(player_name):
            if command == "buy":
                if arg2 in item_prices:
                    price = item_prices[arg2]*arg3
                    amount = users[user_id].takemoney(int(price))
                    if not amount:
                        ctx.reply(f"Not enough money, price: {price}")
                        return
                    else:
                        item_id = f"minecraft:{arg2}"
                        command = f"give {player_name} {item_id} {arg3}"
                        response = mcr.command(command)
                        await ctx.reply(response)
                        return
                elif arg2 in potion_effects:
                    price = potion_effects[arg2]*arg3
                    amount = users[user_id].takemoney(int(price))
                    if not amount:
                        ctx.reply(f"Not enough money, price: {price}")
                        return
                    else:
                        item_id = f"minecraft:potion[potion_contents={{potion:'minecraft:{arg2}'}}]"
                        command = f"give {player_name} {item_id} {arg3}"
                        response = mcr.command(command)
                        await ctx.reply(response)
                        return
                else:
                    await ctx.reply("Item not available")
                    return
            if command == "sell":
                if arg2 in sell_prices:
                    items = itemcount(player_name, arg2)
                    if items >= arg3:
                        command = f"clear {player_name} minecraft:{arg2} {arg3}"
                        response = mcr.command(command)
                        users[user_id].givemoney(sell_prices[arg2]*arg3)
                        await ctx.reply(f"{arg3} items sold, {response}")
                        return
                    else:
                        await ctx.reply(f"not enough items in player inventory {items}/{arg3}")
                        return
                else:
                    await ctx.reply(f"Can't sell this item")
                    return
                return
        else:
            await ctx.reply(f"Player must be online on the server, {player_name} not found")
            return
    else:
        await ctx.reply("Player not registered, use `!season3 register <minecraft nickname>`")
        return



@bot.command()
async def season3command(ctx, *, command):
    if await UserCheck(ctx):
        async with ctx.typing():
            # Connect to Minecraft server using RCON
            # Send command to Minecraft server
            response = mcr.command(command)

            # Split response into chunks if it's too long
            response_chunks = split_message(response)

            # Send each chunk separately
            for chunk in response_chunks:
                await ctx.send(chunk)


@bot.command()
async def seeinventory(ctx, *, nickname):
    if is_player_online(nickname):
        response = inventorycheck(nickname)
        await ctx.reply(response)
    else:
        await ctx.reply("Player not found")


def inventorycheck(nickname):
    try:
        # Execute the data command to list player's inventory
        command = f"data get entity {nickname} Inventory"
        response = mcr.command(command)

        # Print the response (inventory contents)
        print(response)
        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error"


def itemcount(nickname, item):  # returns integer
    # /clear <target> <item> 0 returns number of items in inventory
    response = mcr.command(f"clear {nickname} {item} 0")
    print(response)
    parts = response.split()
    if parts[0] == "No":
        return 0
    else:
        return int(parts[1])


def is_player_online(player):
    # Retrieve list of online players as a string
    online_players = mcr.command('list')

    # Check if the player is in the list of online players
    if player in online_players:
        return True
    else:
        return False
