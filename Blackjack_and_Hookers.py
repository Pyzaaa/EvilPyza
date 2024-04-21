import random
import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)
# Remove the default help command -need to remove it to join 2 bots together
bot.remove_command('help')


standard_deck = {
    '2 of Hearts': 2,
    '3 of Hearts': 3,
    '4 of Hearts': 4,
    '5 of Hearts': 5,
    '6 of Hearts': 6,
    '7 of Hearts': 7,
    '8 of Hearts': 8,
    '9 of Hearts': 9,
    '10 of Hearts': 10,
    'Jack of Hearts': 10,
    'Queen of Hearts': 10,
    'King of Hearts': 10,
    'Ace of Hearts': 11,

    '2 of Diamonds': 2,
    '3 of Diamonds': 3,
    '4 of Diamonds': 4,
    '5 of Diamonds': 5,
    '6 of Diamonds': 6,
    '7 of Diamonds': 7,
    '8 of Diamonds': 8,
    '9 of Diamonds': 9,
    '10 of Diamonds': 10,
    'Jack of Diamonds': 10,
    'Queen of Diamonds': 10,
    'King of Diamonds': 10,
    'Ace of Diamonds': 11,

    '2 of Clubs': 2,
    '3 of Clubs': 3,
    '4 of Clubs': 4,
    '5 of Clubs': 5,
    '6 of Clubs': 6,
    '7 of Clubs': 7,
    '8 of Clubs': 8,
    '9 of Clubs': 9,
    '10 of Clubs': 10,
    'Jack of Clubs': 10,
    'Queen of Clubs': 10,
    'King of Clubs': 10,
    'Ace of Clubs': 11,

    '2 of Spades': 2,
    '3 of Spades': 3,
    '4 of Spades': 4,
    '5 of Spades': 5,
    '6 of Spades': 6,
    '7 of Spades': 7,
    '8 of Spades': 8,
    '9 of Spades': 9,
    '10 of Spades': 10,
    'Jack of Spades': 10,
    'Queen of Spades': 10,
    'King of Spades': 10,
    'Ace of Spades': 11
}


def surrender():
    print("Lost")
    #quit()
    pass


def stop(hand):
    score = 0
    i = 0
    while i < len(hand):
        if standard_deck[hand[i]] == 11 and len(hand) > 1 and standard_deck[hand[-1]] != 11:
            hand[i], hand[-1] = hand[-1], hand[i]
        if standard_deck[hand[i]] == 11 and score + 11 > 21:
            score += 1
        else:
            score += standard_deck[hand[i]]
        i += 1
    if score == 21:
        print("**************  Won  **************")
        score = "**Won**"
    elif score > 21:
        print("******************* Lost ***************")
        score = "**Lost**"
    else:
        print(f"****************** {score} ****************")
    hand = []
    return hand, score


def hit(playing_deck, hand):
    random_card = random.choice(playing_deck)
    hand.append(random_card)
    playing_deck.remove(random_card)
    #print(hand)
    # print(playing_deck.keys())
    return hand


def hithandler(user_id):
    returned = hit(Players[user_id].playerdeck,Players[user_id].hand)
    #print(returned)
    return returned


class Table:
    tabledeck = list(standard_deck.keys())
    Players = {}

    def __init__(self, id, creator_id):
        self.id = id
        Players.update({creator_id: Player(creator_id)})


class Player:
    hand = []
    playerdeck = list(standard_deck.keys())
    wins = 0
    loses = 0

    def __init__(self, id):
        self.id = id

    def __str__(self):
        return f"{self.id}"


if __name__ == "__main__":
    Players = {}
    id = 6969
    Players.update({id: Player(id)})
    print(Players[id])

    hit(Players[id].playerdeck, Players[id].hand)


    def Blackjack():
        hand = []
        while True:
            # print(hand)
            playing_deck = list(standard_deck.keys())
            whatnow = input("What now? (hit) (stop) (surrender): \n")
            if whatnow == "hit":
                hand = hit(playing_deck, hand)
            elif whatnow == "stop":
                hand = stop(hand)
            elif whatnow == "surrender":
                surrender()
                hand = []


    Blackjack()

Tables = {}
Players = {}
def create_player(id):
    Players.update({id: Player(id)})
    Players[id].hand.clear()
    Players[id].playerdeck = list(standard_deck.keys())
    print(Players[id])
    return Players[id]


@bot.command()
async def playblackjack(ctx):
    user_id = ctx.author.id
    returned=create_player(user_id)

    await ctx.reply(f"Created player:{returned}")

@bot.command()
async def create_table(ctx):
    user_id = ctx.author.id
    newid = len(Tables)+1
    Tables.update({newid:Table(newid,user_id)})
    returned=create_player(user_id)
    await ctx.reply(f"Created new table {newid} with owner :{returned}")

@bot.command()
async def surrenderd(ctx):
    user_id = ctx.author.id
    Players[user_id].hand.clear()
    Players[user_id].playerdeck = list(standard_deck.keys())


@bot.command()
async def stopd(ctx):
    user_id = ctx.author.id
    Players[user_id].hand, returned = stop(Players[user_id].hand)
    Players[user_id].playerdeck = list(standard_deck.keys())
    await ctx.reply(f"{returned}")


@bot.command()
async def hitd(ctx):
    user_id = ctx.author.id
    returned = hithandler(user_id)
    await ctx.reply(f"{returned}")




