import pickle
import datetime
import logging
import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)
# Remove the default help command -need to remove it to join 2 bots together
bot.remove_command('help')

logging.basicConfig(filename='data/log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

users = {}

FILE_PATH = "data/users_data.pkl"


class User:
    def __init__(self, userid, date):
        self.id = userid
        self.money = 100
        self.mex = 1
        self.last_income_date = date
        users.update({self.id: self})

    def __str__(self):
        return f"Money: {self.money}\nCurrent eco: {self.mex} \nLast income: {datetime.datetime.fromtimestamp(self.last_income_date).strftime('%Y-%m-%d - %H:%M')}"

    def income(self, date):
        if self.last_income_date + 86400 < date:
            self.money += self.mex * 20

    def transfermoney(self, target, amount):
        if self.money >= amount:
            users[target].money += amount
            self.money -= amount

    def addmex(self):
        if self.money > 3_600:
            self.money -= 3_600
            self.mex += 1
            return f"mex added, currently: {self.mex}"
        else:
            return f"insufficient eco: {self.money}/3600"

    def addarray(self):
        if self.money > 46_000:
            self.money -= 46_000
            self.mex += 14
            return f"mex array added, currently: {self.mex}"
        else:
            return f"insufficient eco: {self.money}/46 000"

    def addparagon(self):
        if self.money > 2_502_000:
            self.money -= 2_502_000
            self.mex += 1000
            return f"**Paragon built**, currently: {self.mex}"
        else:
            return f"insufficient eco: {self.money}/2 502 000"

def usermaker(userid, timestamp):
    if userid in users:
        logging.info(f'User {userid} already exists')
        return "user already exists"
    else:
        User(userid, timestamp)
        logging.info(f'Users created {userid}')
        saveusers()
        return "New user added"


# Loading and saving to file


def saveusers():
    with open(FILE_PATH, 'wb') as f:
        pickle.dump(users, f)
        logging.info('Users data saved successfully.')


def loadusers():
    try:
        with open(FILE_PATH, 'rb') as f:
            global users
            users = pickle.load(f)

            logging.info(f'Users data loaded successfully, {len(users)} loaded.')
    except EOFError:
        print("EOF Error")
        logging.info(f'EOF Error')


def get_command_date(ctx):
    # Extract the timestamp when the command was invoked
    timestamp = ctx.message.created_at.timestamp()
    return timestamp


def user_info(user_id, timestamp):
    users[user_id].income(timestamp)
    returned = users[user_id]
    return returned


if __name__ == "__main__":
    newuser = User(6969, date="2024, 4, 24")

    saveusers()
    loadusers()

    for user_id, user in users.items():
        print("User ID:", user_id)
        print("Money:", user.money)
        print("mex: ", user.mex)
        print("last income date:", user.last_income_date)
        print()

# EXECUTE FROM HERE
loadusers()


@bot.command(help="Economy command")
async def eco(ctx, arg="", user_mention: discord.User = '', amount=0):
    timestamp = get_command_date(ctx)
    user_id = ctx.author.id
    if user_id not in users:
        # creates and saves user if no user is found
        returned = usermaker(user_id, timestamp)
        await ctx.reply(f"No user found, creating new user\n {returned}")
    if arg == "add":
        # creates and saves user, not needed for now
        returned = usermaker(user_id, timestamp)
        saveusers()  # saves user-state after operation
        await ctx.reply(returned)
    elif arg == "addmex":
        returned = users[user_id].addmex()
        saveusers()  # saves user-state after operation
        await ctx.reply(returned)
    elif arg == "addarray":
        returned = users[user_id].addarray()
        saveusers()  # saves user-state after operation
        await ctx.reply(returned)
    elif arg == "addparagon":
        returned = users[user_id].addparagon()
        saveusers()  # saves user-state after operation
        await ctx.reply(returned)
    elif arg == "transfer":
        if isinstance(user_mention, (discord.User, discord.Member)):
            users[user_id].transfermoney(int(user_mention.id), amount)
            saveusers()  # saves user-state after operation
            await ctx.send(f"Transfering {amount} to {user_mention.mention}")
        elif user_mention.id not in users:
            await ctx.send(f"User {user_mention} is not created")
        else:
            await ctx.send(f"User {user_mention} not found\n Correct syntax `!eco transfer @user <amount>`")

    else:
        returned = user_info(user_id, timestamp)
        await ctx.reply(returned)


