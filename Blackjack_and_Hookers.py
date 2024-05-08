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
    busted = False
    pool = 0

    def __init__(self, id):
        self.id = id

    def __str__(self):
        return f"{self.id}"


class Table:
    tabledeck = list(standard_deck.keys())
    tablehand = []
    Players = {}
    still_playing = []
    turn = 0  # first player to have a turn will be player with index 0 on still_playing list
    started = False

    def __init__(self, id, creator_id):
        self.id = id
        self.ownerid = creator_id
        create_player(creator_id)
        self.Players.update({creator_id: Player(creator_id)})

    def remove(self):
        Tables.pop(self.id)

    def join(self, player):
        if not self.started:
            playerid = create_player(player)
            self.Players.update({playerid: Player(playerid)})
            return playerid
        else:
            return False

    def leave(self, player_id):
        self.Players.pop(player_id)
        if not self.Players:
            self.remove()

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
        self.still_playing = list(self.Players.keys())  # populate turn tracking list with players that still play
        self.turn = 0  # set first player to index 0
        return returned

    def next_turn(self):
        # fixme: this will be pain to use here
        if not self.still_playing:  # if no more players are playing, make dealer play and end game
            self.dealerturn()
            return
        if self.turn == len(self.still_playing):
            self.turn = 0
        else:
            self.turn += 1

    def hit(self, player):
        playerscore = count(hit(self.tabledeck, self.Players[player].hand))  # hit zwraca hand'a
        self.next_turn()
        if playerscore > 21:
            self.still_playing.remove(player)
            self.Players[player].busted = True
            return f"{self.Players[player].hand}, score: {playerscore}, **Busted**"
        else:
            return f"{self.Players[player].hand}, score: {playerscore}"

    def stop(self, player):
        self.Players[player].score = count(self.Players[player].hand)
        self.still_playing.remove(player)
        self.next_turn()
        return f"Hand: {self.Players[player].hand}, {self.Players[player].score}"

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
            if dealerscore > 21:
                # TODO: mark all players as winning?
                return "Players win"
        for player in self.Players:
            if dealerscore < self.Players[player].score:
                return f"{player} wins"
            elif dealerscore == self.Players[player].score:
                return f"tie {dealerscore}"
            else:
                return f"{player} Lost: {dealerscore} > {self.Players[player].score}"

    def listplayers(self):
        for p in self.Players.keys():
            print(p)
            return p


Tables = {}
Players = {}


def create_player(id):  # shadows built-in name?
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
async def blackjack(ctx, arg="", arg2=""):
    current_table: Table = None
    user_id = ctx.author.id
    if arg == "":
        await ctx.reply(
            "No argument provided, use `!blackjack create` to create a table, `!blackjack start` to start, `!blackjack hit` and `!blackjack stop` to play")
        return
    if arg == "create":  # create table
        for table in Tables.values():
            if user_id in table.Players:
                await ctx.reply(f"Already playing at table: {table.id} with owner: {table.ownerid}")
                return
        new_id = len(Tables)
        Tables.update({new_id: Table(new_id, user_id)})
        returned = create_player(user_id)
        await ctx.reply(f"Created new table {new_id} with owner :{returned}")
        return
    if arg == "join":
        for table in Tables.values():
            if user_id in table.Players:
                await ctx.reply(f"Already playing at table: {table.id} with owner: {table.ownerid}")
                return
        table_id = int(arg2)
        returned = Tables[table_id].join(user_id)
        if returned:
            await ctx.reply(f"joined table {table_id} as {returned} with owner: {Tables[table_id].ownerid}")
        else:
            await ctx.reply(f"Game has already started")
    for table in Tables.values():
        if user_id in table.Players:
            current_table = table
            break
    if current_table is None:
        await ctx.reply(f"Player {user_id} not found at any table use `!blackjack create` to create a table or `!blackjack join <table ID>` to join a game")
        return
    if arg == "leave":
        current_table.leave(user_id)
    if not current_table.started:
        if arg == "start":  # tables start method
            if user_id != current_table.ownerid:
                await ctx.reply(f"Only table owner can start the table owner: {current_table.ownerid}")
            returned = current_table.start()
            await ctx.send(f"{returned}")
        else:
            await ctx.reply(f"Game created but not started, use `!blackjack start`")
    else:
        # TODO: turn checking here
        if arg == "hit":  # tables hit method
            returned = current_table.hit(user_id)
            await ctx.reply(f"{returned}")

        if arg == "stop":  # tables stop method
            returned = current_table.stop(user_id)
            await ctx.send(f"{returned}")
            current_table.end()  # fixme: quick fix
        # TODO: dealerturn() here?
        # TODO: end here?


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
