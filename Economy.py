import pickle
import datetime
import logging
import discord

from Importedbot import bot

# basic Logging
logging.basicConfig(filename='data/log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
# create users dictionary-database
users = {}
# set filepath for savefile
FILE_PATH = "data/users_data.pkl"

class User:  # User class for user management
    def __init__(self, userid, date):
        self.id = userid
        self.money = 100
        self.mex = 1
        self.last_income_date = date
        users.update({self.id: self})

    def __str__(self):  # for printing user info
        return f"Money: {self.money}\nCurrent eco: {self.mex} \nLast income: {datetime.datetime.fromtimestamp(self.last_income_date).strftime('%Y-%m-%d - %H:%M')}"

    def takemoney(self, amount):
        if self.money >= amount:
            self.money -= amount
            saveusers()  # saves user-state after operation
            return amount
        else:
            return False

    def givemoney(self, amount):
        self.money += amount
        saveusers()  # saves user-state after operation
        pass

    def income(self, date):  # generate money
        print(date)
        print(self.last_income_date)
        if self.last_income_date + 86400 < date:  # can only be used once /24h
            self.money += self.mex * 20
            self.last_income_date = date
            saveusers()  # saves user-state after operation

    def transfermoney(self, target, amount):  # transfer money to another user
        if self.money >= amount:
            users[target].money += amount
            self.money -= amount

    def addmex(self):  # better income
        if self.money > 3_600:
            self.money -= 3_600
            self.mex += 1
            return f"mex added, currently: {self.mex}"
        else:
            return f"insufficient eco: {self.money}/3600"

    def addarray(self):  # more expensive, better return
        if self.money > 46_000:
            self.money -= 46_000
            self.mex += 14
            return f"mex array added, currently: {self.mex}"
        else:
            return f"insufficient eco: {self.money}/46 000"

    def addparagon(self):  # epic income
        if self.money > 2_502_000:
            self.money -= 2_502_000
            self.mex += 1000
            return f"**Paragon built**, currently: {self.mex}"
        else:
            return f"insufficient eco: {self.money}/2 502 000"


def usermaker(userid, timestamp): # for creating users
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


def get_command_date(ctx):  # nie wiem po chuj robić to osobną funkcją, anyways
    # Extract the timestamp when the command was invoked
    timestamp = ctx.message.created_at.timestamp()
    return timestamp


def user_info(user_id, timestamp):  # sprawdzenie usera, danie mu hajsu, zwrócenie userinfo do printowania na chat
    users[user_id].income(timestamp)
    returned = users[user_id]
    return returned


if __name__ == "__main__":  # testing
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


@bot.command(help="Economy command")  # wszystko w jednej komendzie żeby nie trzebabyło milion komend wpisywać
async def eco(ctx, arg="", user_mention: discord.User = '', amount=0):  # usermention/amount do transferu, poza tym useless
    timestamp = get_command_date(ctx)
    user_id = ctx.author.id
    if user_id not in users:
        # creates and saves user if no user is found
        returned = usermaker(user_id, timestamp)
        await ctx.reply(f"No user found, creating new user\n {returned}")
        saveusers()  # saves user-state after operation
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
        if isinstance(user_mention, (discord.User, discord.Member)):  # sprawdź czy pingowany user istnieje
            users[user_id].transfermoney(int(user_mention.id), amount)  # i czy ma konto
            saveusers()  # saves user-state after operation
            await ctx.send(f"Transfering {amount} to {user_mention.mention}")
        elif user_mention.id not in users:
            await ctx.send(f"User {user_mention} is not created")
        else:
            await ctx.send(f"User {user_mention} not found\n Correct syntax `!eco transfer @user <amount>`")

    else:  # jeżeli uzyte bez argumentu to wyprintuje info
        returned = user_info(user_id, timestamp)
        await ctx.reply(returned)



''' #for testing purposes only
@bot.command(help="Economy command")
async def takemoney_test(ctx, amount):
    user_id = ctx.author.id
    amount = users[user_id].takemoney(int(amount))
    print(amount)

    print(users[user_id].money)
'''