import random
import discord
from EvilPyzaValidate import UserCheck
import subprocess
from Importedbot import bot, split_message, discorduser_mention, logging
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
        logging.info(f'Minecraft players data saved')


def loadplayers():
    try:
        with open(FILE_PATH, 'rb') as f:
            global Playerlist
            Playerlist = pickle.load(f)
            logging.info(f'Minecraft players data loaded successfully, {len(Playerlist)} loaded.')
    except EOFError:
        print("EOF Error")
        logging.warning(f'EOF ERROR while loading player data')


loadplayers()

sold_stats = {}
STATS_PATH = "data/minecraft_sold_stats.pkl"


def savestats():
    with open(STATS_PATH, 'wb') as f:
        pickle.dump(sold_stats, f)
        logging.info(f'Minecraft sell data saved')


def loadstats():
    try:
        with open(STATS_PATH, 'rb') as f:
            global sold_stats
            sold_stats = pickle.load(f)
            logging.info(f'Minecraft sell data loaded successfully, {len(sold_stats)} loaded.')
    except EOFError:
        print("EOF Error")
        logging.warning(f'EOF ERROR while loading sell data')


loadplayers()
loadstats()

scoreboards = ["KillCount", "Wyjebki"]
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
    "glass": 5,
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
    "totem_of_undying": 400,
    "candle": 5,
    "painting": 10
}
sell_prices = {
    "obsidian": 1,
    "emerald": 5,
    "diamond": 15,
    "netherite_ingot": 150,
    "nether_star": 180,
    "beacon": 130,
    "creeper_head": 60,
    "zombie_head": 50,
    "skeleton_skull": 50,
    "wither_skeleton_skull": 50,
    "dragon_head": 10,
    "elytra": 100,
    "netherite_upgrade_smithing_template": 150,
    "golden_apple": 30,
    "enchanted_golden_apple": 300,
    "totem_of_undying": 20
}

potion_effects = {
"fire_resistance": 200,
"strength": 200,
"invisibility": 200,
"night_vision": 200,
"slow_falling": 200,
"water_breathing": 200,
"speed": 200
}

############## /commands don't work on bukkit cause why not LMAO
@bot.command()
async def season3(ctx, command="", arg2=None, arg3=''):
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
    if command == "switch":
        switch_scoreboard()
        await ctx.send("Scoreboard switched")
        return
    if command == "team":
        if not arg2:
            await ctx.reply(f"Minecraft team management, use `team add, join, leave` to manage teams, for team color change @Pyzu cause he's too lazy to code it in")
        if arg2 == "add":
            if arg3 and not '':
                await ctx.reply(f"Creating team with name {arg3}")
                mcr.command(f"team add {arg3}")
            else:
                await ctx.reply(f"No team name found: {arg3}")
        if arg2 == "join":
            if is_player_online(Playerlist[user_id]):
                if arg3 and not '':
                    await ctx.reply(f"Joining team {arg3}")
                    mcr.command(f"team join {arg3} {Playerlist[user_id]}")
                else:
                    await ctx.reply(f"No team name found: {arg3}")
            else:
                await ctx.reply(f"Player not found online on the server")
        if arg2 == "leave":
            if is_player_online(Playerlist[user_id]):
                await ctx.reply(f"Leaving team")
                mcr.command(f"team leave {Playerlist[user_id]}")
            else:
                await ctx.reply(f"Player not found online on the server")
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
                logging.info(f"Registered player {await discorduser_mention(user_id)} as {arg2}")
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
            logging.info(f"Player {await discorduser_mention(user_id)}: {removed} unregistered")
            return
        else:
            await ctx.reply("Player not found in registered players list")
            return
    elif command == "price":
        returned = ""
        if arg2 and arg2 in item_prices.keys():
            # return item price instead of whole list
            returned = f"{arg2} costs: {item_prices[arg2]}/per item\n"
        if arg2 and arg2 in potion_effects.keys():
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
        shop += "***Potion Prices:***\n"
        for item, price in potion_effects.items():
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
    if command not in ["buy", "sell", "lock"]:
        await ctx.reply(f"Unknown command {command}")
        return
    elif user_id in Playerlist:
        player_name = Playerlist[user_id]
        try:
            arg3 = int(arg3)
        except:
            arg3 = 1
        if arg3 < 1:
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
            elif command == "sell":
                if arg2 in sell_prices:
                    items = itemcount(player_name, arg2)
                    if items >= arg3:
                        command = f"clear {player_name} minecraft:{arg2} {arg3}"
                        response = mcr.command(command)
                        users[user_id].givemoney(sell_prices[arg2]*arg3)
                        await ctx.reply(f"{arg3} items sold, {response}")
                        if arg2 not in sold_stats:
                            sold_stats[arg2] = arg3
                            savestats()
                        else:
                            sold_stats[arg2] += arg3
                            savestats()
                        return
                    else:
                        await ctx.reply(f"not enough items in player inventory {items}/{arg3}")
                        return
                else:
                    await ctx.reply(f"Can't sell this item")
                    return
                return
            elif command == "lock":
                if arg2:
                    price = 20
                    amount = users[user_id].takemoney(int(price))
                    if not amount:
                        ctx.reply(f"Not enough money, price: {price}")
                        return
                    else:
                        command = f"give {player_name} chest[minecraft:lock='{arg2}']"
                        response = mcr.command(command)
                        await ctx.reply(f"{response} locked with item name: {arg2}")
                        return
                else:
                    ctx.reply(f"No Key lock argument provided")
                    return
        else:
            await ctx.reply(f"Player must be online on the server, {player_name} not found")
            return
    else:
        await ctx.reply("Player not registered, use `!season3 register <minecraft nickname>`")
        return



@bot.command()
async def season3command(ctx, *, command):
    logging.info(f"User {ctx.author} attempted to use: {command}")
    if await UserCheck(ctx):
        async with ctx.typing():
            # Connect to Minecraft server using RCON
            # Send command to Minecraft server
            response = "Response: \n"
            response = mcr.command(command)
            logging.info(f"{command} execution result: {response}")

            # Split response into chunks if it's too long
            response_chunks = split_message(response)

            # Send each chunk separately
            for chunk in response_chunks:
                #print (f"Printing chunk: {chunk}")
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


def switch_scoreboard():
    popped = scoreboards.pop(0)
    scoreboards.append(popped)
    mcr.command(f'scoreboard objectives setdisplay sidebar {popped}')
    print(f"switched scoreboard to {popped}")
