import random
import discord
from EvilPyzaRoles import CHANNEL_ID

from Importedbot import bot
KASYNO = 1232060058305564722

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

def count(hand):
    score = 0
    i = 0
    sorted_hand = sorted(hand, key=lambda a: a[0] == "A")  # lambda checks if element starts with A, if it does return False, if it doesn't True, Trues come before Falses in sorting
    while i < len(hand):
        if standard_deck[sorted_hand[i]] == 11 and score + 11 > 21:  # if ace is last, count it as 1 not to lose
            score += 1
        else:
            score += standard_deck[sorted_hand[i]]
        i += 1
    return score

def stop(hand):
    score = count(hand)

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


class Player:
    hand = []
    playerdeck = list(standard_deck.keys())
    wins = 0
    loses = 0
    score = 0

    def __init__(self, id):
        self.id = id

    def __str__(self):
        return f"{self.id}"


class Table:
    tabledeck = list(standard_deck.keys())
    tablehand = []
    Players = {}
    started = False

    def __init__(self, id, creator_id):
        self.id = id
        self.ownerid = creator_id
        create_player(creator_id)
        self.Players.update({creator_id: Player(creator_id)})

    def join(self, player):
        if not self.started:
            playerid = create_player(player)
            self.Players.update({playerid: Player(playerid)})
            return playerid
    #   else:
    #        return "Game in progress"

    def start(self):
        self.started = True
        returned = "**Game started**: \n"

        for p in self.Players.values():  # clears all players at the table and deals them 2 cards
            p.score = 0
            p.hand.clear()
            returned += f"Player **{p.id}** hand: "
            self.hit(p.id)
            returned += f"{self.hit(p.id)}\n"

        hit(self.tabledeck, self.tablehand)  # deals 2 cards to dealer and prints one and another as hidden
        hit(self.tabledeck, self.tablehand)
        returned += f"Table hand: {self.tablehand[1]}, *hidden card*"
        return returned

    def hit(self, player):
        playerscore = count(hit(self.tabledeck, self.Players[player].hand))  # hit zwraca hand'a
        if playerscore > 21:
            return f"{self.Players[player].hand}, score: {playerscore}, **Busted**"
        else:
            return f"{self.Players[player].hand}, score: {playerscore}"

    def stop(self, player):
        self.Players[player].score = count(self.Players[player].hand)

        # fixme: this works only for 1 player, need to make queue with checking if player is playing or stopped already
        dealerscore = self.dealerturn()
        if self.Players[player].score > 21:  # fixme: this should be checked and ended before
            return "Already busted"
        if dealerscore > 21:
            return "Players win"
        elif dealerscore < self.Players[player].score:
            return f"{player} wins"
        elif dealerscore == self.Players[player].score:
            return f"tie {dealerscore}"
        else:
            return f"{player} Lost: {dealerscore} > {self.Players[player].score}"
        # return self.Players[player].score

    def play(self):
        pass

    def end(self):
        self.tabledeck = list(standard_deck.keys())
        self.tablehand.clear()
        self.started = False
        pass

    def dealerturn(self):
        dealerscore = count(self.tablehand)
        while dealerscore < 17:
            hit(self.tabledeck, self.tablehand)
            print(f"dealer draws {self.tablehand}")  # TODO: print that to chat as well?
            dealerscore = count(self.tablehand)
        return dealerscore

    def listplayers(self):
        for p in self.Players.keys():
            print(p)
            return p








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
    print(f"{Players[id]} joined game")
    return Players[id]


@bot.command()
async def playblackjack(ctx):
    if ctx.channel.id in (KASYNO, CHANNEL_ID):
        user_id = ctx.author.id
        returned = create_player(user_id)
        hand = Players[user_id].hand
        hit(Players[user_id].playerdeck, Players[user_id].hand)
        hit(Players[user_id].playerdeck, Players[user_id].hand)

        await ctx.reply(f"Created player:{returned}, use hitd, stopd to play, your hand: {hand}")
    else:
        await ctx.reply("idź na #kasyno-evilpyzy")


@bot.command()
async def blackjack(ctx, arg=""):
    current_table: Table = None
    user_id = ctx.author.id
    if arg == "":
        await ctx.reply(
            "No argument provided, use `!blackjack create` to create a table, `!blackjack start` to start, `!blackjack hit` and `!blackjack stop` to play")
        return
    if arg == "create":  # create table
        new_id = len(Tables)
        for table in Tables.values():
            if user_id in table.Players:
                await ctx.reply(f"Already playing at table: {table.id} with owner: {table.ownerid}")
                return
        Tables.update({new_id: Table(new_id, user_id)})
        returned = create_player(user_id)
        await ctx.reply(f"Created new table {new_id} with owner :{returned}")
        return

    for table in Tables.values():
        if user_id in table.Players:
            current_table = table
            break
    if current_table is None:
        await ctx.reply(f"Player {user_id} not found at any table use `!blackjack create` to create a table")
        return
    if not current_table.started:
        if arg == "start":  # tables start method
            returned = current_table.start()
            await ctx.send(f"{returned}")
        else:
            await ctx.send(f"Game created but not started, use `!blackjack start`")
    else:
        if arg == "hit":  # tables hit method
            returned = current_table.hit(user_id)
            await ctx.reply(f"{returned}")

        if arg == "stop":  # tables stop method
            returned = current_table.stop(user_id)
            await ctx.send(f"{returned}")
            current_table.end()  # quick fix


'''

@bot.command()
async def join_table(ctx, *, arg):
    user_id = ctx.author.id
    arg = int(arg)
    returned = Tables[arg].join(user_id)
    await ctx.reply(f"joined table {arg} as {returned} with owner: {Tables[arg].ownerid}")



@bot.command()
async def start_table(ctx, *, arg):
    user_id = ctx.author.id
    arg = int(arg)
    Tables[arg].start()
    await ctx.reply(f"table {arg} starting")

@bot.command()
async def listplayers(ctx, *, arg):
    arg = int(arg)
    returned = Tables[arg].listplayers()

    # user = await bot.fetch_user(returned) # Generalnie to to powinno zwrócić usera
    # user.mention  # a to powinno spingować tego usera, tak samo jak pinguje !Farmazon, ale nie działa XD

    await ctx.reply(f"table {arg} has {returned}")


@bot.command()
async def surrenderd(ctx):
    user_id = ctx.author.id
    try:
        Players[user_id].hand.clear()
        Players[user_id].playerdeck = list(standard_deck.keys())
    except KeyError:
        await ctx.reply(f"player {user_id} doesn't exist")
'''

@bot.command()
async def stopd(ctx):
    if ctx.channel.id in (KASYNO, CHANNEL_ID):
        user_id = ctx.author.id
        try:
            Players[user_id].hand, returned = stop(Players[user_id].hand)
            Players[user_id].playerdeck = list(standard_deck.keys())
        except KeyError:
            await ctx.reply(f"player {user_id} doesn't exist")
        else:
            await ctx.reply(f"{returned}")
            hit(Players[user_id].playerdeck, Players[user_id].hand)
            hit(Players[user_id].playerdeck, Players[user_id].hand)

            hand = Players[user_id].hand
            await ctx.reply(f"Play again?, use hitd, stopd to play, your hand: {hand}")
    else:
        await ctx.reply("idź na #kasyno-evilpyzy")

@bot.command()
async def hitd(ctx):
    if ctx.channel.id in (KASYNO, CHANNEL_ID):
        user_id = ctx.author.id
        try:
            returned = hit(Players[user_id].playerdeck, Players[user_id].hand)
        except KeyError:
            await ctx.reply(f"player {user_id} doesn't exist")
        else:
            await ctx.reply(f"{returned}")
    else:
        await ctx.reply("idź na #kasyno-evilpyzy")

'''
@bot.command()
async def tablestop(ctx, *, arg):
    user_id = ctx.author.id
    arg = int(arg)
    await ctx.reply(f"{Tables[arg].stop(user_id)}")


@bot.command()
async def tablehit(ctx, *, arg):
    user_id = ctx.author.id
    arg = int(arg)
    await ctx.reply(f"{Tables[arg].hit(user_id)}")
'''
