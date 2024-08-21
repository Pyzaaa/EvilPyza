import random
import discord
from Blackjack_and_Hookers import KASYNO, CHANNEL_ID
from Economy import users
from Importedbot import bot
from collections import defaultdict
import json
import os


DATA_FILE = "data/zdrapki_data.json"

zdrapki_data = {
    "playcount": 0,
    "total_bet": 0,
    "highest_bet": 0,
    "win_stats": {
        "0": 0,
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0,
        "7": 0,
        "8": 0,
        "9": 0,
        "69": 0,
        "1r": 0,
        "2r": 0,
        "3r": 0,
        "4r": 0,
        "5r": 0,
    }
}

def update_win_data(key):
    load_data()
    key = str(key)
    if key in zdrapki_data["win_stats"]:
        zdrapki_data["win_stats"][key] += 1
    else:
        print(f"Key {key} not found in win_stats")
    save_data()

def update_play_data(bet):
    load_data()
    key = "playcount"
    if key in zdrapki_data:
        zdrapki_data[key] += 1
    else:
        print(f"Key {key} not found in win_stats")
    key = "total_bet"
    if key in zdrapki_data:
        zdrapki_data[key] += bet
    else:
        print(f"Key {key} not found in win_stats")
    key = "highest_bet"
    if key in zdrapki_data:
        if bet > zdrapki_data[key]:
            zdrapki_data[key] = bet
    else:
        print(f"Key {key} not found in win_stats")
    save_data()

# Load data from file
def load_data():
    global zdrapki_data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            zdrapki_data = json.load(f)
    #print("Loaded data:", zdrapki_data)


# Save data to file
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(zdrapki_data, f, indent=4)

players = {}

class Player():

    def __init__(self, userid):  #
        self.id = userid
        self.session = None
        self.money = 0

    def create_session(self, type, amount):
        try:
            amount = users[self.id].takemoney(int(amount))
        except KeyError:
            return False
        if amount:
            #print(amount)
            self.session = Card(5, amount)
            self.money += self.session.count()
            update_play_data(amount)
            return True
        else:
            return False
        pass

    def end_session(self):
        self.session = None
        won = self.money
        users[self.id].givemoney(int(won))
        self.money = 0
        return won

class Card():
    def __init__(self, size, cost):
        self.main_array = [[None]*size] * size
        self.size = size
        value = 1
        mid = size // 2
        self.cost = cost
        for i in range(len(self.main_array)):
            if i <= mid:
                self.main_array[i] = self.array_maker(size, value + i)
            else:
                self.main_array[i] = self.array_maker(size, size - i)


    @staticmethod
    def array_maker(length, possibilities):
        array = [0] * length
        for i in range(len(array)):
            array[i] = random.randint(0, possibilities)
            if random.randint(1, 300) == 1:
                array[i] = 69
        return array

    def count(self):
        value = 2
        mid = (self.size+1) // 2
        reward = 0
        count_dict = defaultdict(int) # dictionary for occurances of given result
        for i in range(len(self.main_array)):
            if len(set(self.main_array[i])) == 1: #converts the array to set, if set has length of 1, all elements are the same
                update_win_data(str(i+1)+"r")
                if i < mid-1:
                    reward += (i+1) * self.cost * 3
                elif i == mid-1:
                    reward += 20 * self.cost
                else:
                    reward += (self.size - i) * self.cost * 3

            for cell in self.main_array[i]: # szczesliwa myszka
                #print(f"checking {i}, {cell}")
                count_dict[cell] += 1 # add occurance to dictionary
                if cell == 69:
                    reward += 5 * self.cost
                    update_win_data(69)
        # Convert the defaultdict to a regular dictionary
        count_dict = dict(count_dict)
        for num, count in count_dict.items(): # if more than half of all items are the same, add bonus
            if count > 12:
                reward += (num) * self.cost
                update_win_data(num)

        return reward

    def print_card(self):
        i = 1
        mid = (self.size+1) // 2
        printable = "BONUS: 1x: 13x☁️; 2x: 13x⭐; 5x: 1x🐭 \n"
        for array in self.main_array:
            #print(i)
            #print(mid)
            if i < mid:
                printable += str(i*3) + "x: "
            elif i == mid:
                printable += str(20) + "x: "
            else:
                printable += str((self.size - i + 1)*3) + "x: "

            for cell in array:
                printable += "|| " + str(replace_numbers_with_emotes(cell)) + " || "

            printable += "\n"
            i += 1

        return printable



def format_zdrapki_data(data):
    result = f"Total games played: {data['playcount']}\n"
    result += f"Total Bet: {data['total_bet']}\n"
    result += f"Highest Bet: {data['highest_bet']}\n"
    result += "Win Stats by win condition:\n"
    for key, value in data['win_stats'].items():
        result += f"  {format_replacer(key)}: {value}\n"
    return result.strip()

def format_replacer(key):
    if key.isdigit():
        print(f"Key {key} is a number.")
        return replace_numbers_with_emotes(int(key))
    elif key.endswith('r'):
        print(f"Key {key} is a string ending with 'r'.")
    else:
        print(f"Key {key} is neither a number nor a string ending with 'r'.")
    return key

def replace_numbers_with_emotes(numbers):
    # Mapping of numbers to various emotes
    number_to_emote = {
        0: "❤️",  # Heart for 0
        1: "☁️",  # Cloud for 1
        2: "⭐",  # Star for 2
        3: "🌙",  # Moon for 3
        4: "🔥",  # Fire for 4
        5: "🌈",  # Rainbow for 5
        6: "💧",  # Droplet for 6
        7: "🌟",  # Glowing star for 7
        8: "⚡",  # Lightning for 8
        9: "🌺",   # Flower for 9
        69:"🐭", # Szczesliwa myszka for 69
    }

    # Replace each number in the array with its corresponding emote
    emotes = number_to_emote.get(numbers, numbers)

    return emotes

@bot.command()
async def zdrapki(ctx, arg = "", amount=10, type=1):
    user_id = ctx.author.id
    player : Player

    if ctx.channel.id not in (KASYNO, CHANNEL_ID):  # only allowed to play on correct channel
        await ctx.reply("graj tylko na #kasyno-evilpyzy")
        return

    if arg == "help":
        await ctx.reply("use `!zdrapki play [cost- default 10] [game-type(currently only 1) - default 1]` to play, `!zdrapki end` to cashout, `!zdrapki print` to reprint the card again. \n"
                        "for gametype specific help, use `!zdrapki help1` for type 1")
        return
    if arg == "help1":
        await ctx.reply("Zdrapka typu szczęśliwa myszka, 🐭 gdziekolwiek na polu zwraca **koszt x5**. Jeżeli ponad połowa pól ma ten sam symbol to zwraca **koszt x rzadkość symbolu**")
        return
    if user_id not in players:
        player = Player(user_id)
        players[user_id] = player
    else:
        player = players[user_id]
    if arg == "printstats":
        await ctx.send(format_zdrapki_data(zdrapki_data))
        return



    if arg == "play":
        if player.session:
            await ctx.reply(f"Already playing, to get new card use `!zdrapki end`")
            await ctx.reply(player.session.print_card())
            return
        if not player.create_session(type, amount):
            await ctx.reply(f"Not enough money")
        else:
            await ctx.reply(f"Zdrapuj!: \n")
            await ctx.reply(player.session.print_card())
            # quick ending
            #received = player.end_session()
            #await ctx.reply(f"reward received: ||{received}||")


    if not player.session:
        await ctx.reply(f"No active session found, use `!zdrapki help` for help or `!zdrapki play`")
        return
    elif arg == "end":
        received = player.end_session()
        await ctx.reply(f"reward received: {received}")

    elif arg == "print":

        await ctx.reply(player.session.print_card())


