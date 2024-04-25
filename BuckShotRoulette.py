import random
import discord
from discord.ext import commands
from Blackjack_and_Hookers import KASYNO, CHANNEL_ID
from Economy import users

intents = discord.Intents.default()

intents.reactions = True
intents.members = True
intents.guilds = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)
# Remove the default help command -need to remove it to join 2 bots together
bot.remove_command('help')

SHELLS = ["blank", "live"]  # shells defined
sr_players = {}  # dictionary for players in game
sessions = {}  # dictionary for sessions
dealers = {}   # dictionary for players(dealers) in game


class Player:
    score = 0  # TODO: keep score, need to change code not to delete players after game.

    def __init__(self, userid, health, opponent):  # dealerID is 69
        self.id = userid
        self.health = health  # TODO: health can be static with a rand function inclued instead of this?
        self.opponent = opponent  # for finding who the player plays against

    def __str__(self):
        return f"{self.id}"


class Dealer(Player):  # child class for creating multiple dealers to play against
    isdealer = True

    async def dealerplay(self, session, ctx):  # dealerplay function moved here, id=69 changed to self.id
        target = session.Player1
        while session.in_use and session.turn == self.id:  # check if game is on and it's still dealers turn
            if session.magazine.count('live') >= session.magazine.count('blank'):  # dealer knows number of shells but not their order
                returned = "Dealer move:\n **YOU**\n" + session.shoot(target)      # if there are <= lives than blanks he will shoot at player
                await ctx.reply(f"{returned}")

            else:
                if session.magazine[0] == 'live':   # if live in chamber dealer will print gif before shooting himself
                    returned = "Dealer move:\n Self:" + session.shoot(self.id)
                    await ctx.reply(f"{returned}", file=discord.File('shotgungifs/dealersuicide.gif'))
                elif not session.magazine:  # if mag is empty, dealer will reload and give it to the player, might not be needed since #shoot handles that
                    session.load()
                else:  # if dealer shoots himself with blank he will print it and have another turn in a loop
                    returned = "Dealer move:\n Self:" + session.shoot(self.id)
                    await ctx.reply(f"{returned}")
            if not session.in_use:
                "Game ended"
        return "Dealer turn ended"


class Shotgun:
    magazine = []  # mag list for shells
    turn = 69  # for turntracking
    in_use = False  # for checking if game is started
    Player2 = 69  # if unchanged, Player 2 is a dealer, there will only be one dealer so more than 1 dealer game will bug
    pool = 0  # variable for keeping bet pool

    def __init__(self, gameid):  # when session created, creator will be player 1, his ID will be game ID
        self.id = gameid
        self.Player1 = gameid

    def start(self, playerid, opponent):  # creates players and starts session # TODO: long af, make it shorter somehow?
        if not self.in_use:  # shouldn't try to start when game already started
            self.magazine.clear()  # clear magazine if it's not empty for some reason
            if opponent == 69:  # if opponent is a dealer, create Dealer object instead of Player object
                opponent = len(dealers)
                sr_players.update(
                    {playerid: Player(playerid, random.choice(range(2, 4)), opponent)})  # create player 1 object
                sr_players.update({sr_players[playerid].opponent: Dealer(sr_players[playerid].opponent, sr_players[playerid].health, playerid)}) # create player 2 object using player 1, could also use opponent arg i guess
                dealers.update({opponent: sr_players[opponent]})
                self.pool *= 2
            else:
                sr_players.update({playerid: Player(playerid, random.choice(range(2, 4)), opponent)})  # create player 1 object
                sr_players.update({sr_players[playerid].opponent: Player(sr_players[playerid].opponent, sr_players[playerid].health, playerid)}) # create player 2 object using player 1, could also use opponent arg i guess
            self.Player2 = sr_players[playerid].opponent  # save opponent as player 2
            self.in_use = True  # marks session as started
            return self.load()
        else:
            return "Already in use"

    def load(self):  # loads random number of shells into magazine in random order
        number = random.choice(range(2, 9))  # number of shells
        i = 0
        while i <= number:
            self.magazine.append(random.choice(SHELLS))
            i += 1
        lives = self.magazine.count('live')
        while lives == len(self.magazine) or lives == 0:  # if there's only one type of shells, change some
            self.magazine[random.choice(range(number))] = 'blank'
            self.magazine[random.choice(range(number))] = 'live'
            lives = self.magazine.count('live')  # recount live shells
        mag_content = f"{lives} live shells, {len(self.magazine) - lives} blanks"  # for printing mag contents
        self.turn = self.id  # Set player 1 as player, idk if it should still be there
        print(mag_content)
        return mag_content  # return printable mag contents for other functions

    def shoot(self, target):  # shoots target, checks if they still live TODO: cleanup
        if self.magazine and self.magazine[0] == "live":
            sr_players[target].health -= 1  # reduce health on live shell
            self.magazine.pop(0)  # remove expended shell
            self.turnswitch()  # swap player turns
            if sr_players[target].health == 0:
                self.in_use = False  # end session if player dies
                return f"***gunshot*** \n**{target} is dead**"
            if not self.magazine:  # reload magazine on empty
                loaded = self.load()
                return f"***gunshot*** \n {loaded} Your turn: {str(self.turn)}"
            return f"***gunshot*** \n Your turn: {str(self.turn)}"
        elif self.magazine and self.magazine[0] == "blank":
            self.magazine.pop(0)  # remove expended shell
            if target != self.turn:
                self.turnswitch()  # switch player turns if player tried to shoot opponent
            if not self.magazine:
                loaded = self.load()  # reload magazine on empty
                return f"***click*** \n {loaded} Your turn: {str(self.turn)}"
            return "*click*\nYour turn: " + str(self.turn)

    def turnswitch(self):  # switching current player
        if self.turn == self.Player1:
            self.turn = self.Player2
        else:
            self.turn = self.Player1
        return self.turn

    def whowins(self):  # check who won and return it
        if sr_players[self.Player1].health < 1:
            return self.Player2
        elif sr_players[self.Player2].health < 1:
            return self.Player1
        else:
            return False

    def end(self, target):  # on game ended remove players and the session
        if target in sessions:
            del sessions[target]
        elif sr_players[target].opponent in sessions:
            del sessions[sr_players[target].opponent]
        self.pool = 0  # reset pool to 0 when game ends
        del sr_players[target].opponent
        del sr_players[target]

# dealerplay removed


if __name__ == "__main__":  # testing
    Player1 = Player(6969, 2)
    sr_players.update({'6969': Player1})


def getsession(user_id):
    try:
        if user_id in sessions:
            session = sessions[user_id]
        elif sr_players[user_id].opponent in sessions:  # when the other player has a turn, should use only session. methods after that point
            session = sessions[sr_players[user_id].opponent]  # set session as the session where user is the opponent of the host
        else: return False
        return session
    except KeyError:
        print("No user_id in sessions, returning False")
        return False

@bot.command()
async def playshotgun(ctx, arg="", user_mention: discord.User = 69):  # if no user mentioned, opponent will be the dealer
    user_id = ctx.author.id
    if ctx.channel.id in (KASYNO, CHANNEL_ID):  # only allowed to play on correct channel
        global sessions  # use global sessions dict
        if arg == "create":  # create session
            session = Shotgun(user_id)
            if user_id in sessions:  # if there's a session already, delete it
                del sessions[user_id]
                sessions[user_id] = session
            else:  # if no session exists, just add it
                sessions[user_id] = session
            await ctx.reply(
                "Game created, use `!playshotgun start [@user](optional)` to play:\nPlay using `!playshotgun self` and `!playshotgun opponent`")
            return
        if arg == "start":  # starting session and creating players
            if user_id in sessions:
                session = sessions[user_id]
            else:
                await ctx.reply("Game not created, use `!playshotgun create`")
                return
            if sessions[user_id].in_use:
                await ctx.reply("You are already playing")
                return
            target = user_mention
            if target != 69:
                target = target.id
                if target == user_id:  # if player pinged himself, play against dealer anyway
                    target = 69
            returned = session.start(user_id, target)
            await ctx.reply(f"Game ready: \n {returned}\nhealth: {sr_players[user_id].health}", file=discord.File('shotgungifs/The_Dealer_29.gif'))
            # discorduser = await bot.fetch_user(int(session.turn))  # fixme should mention user instead of user_id, doesn't work
            # await ctx.send(f'Your turn: {discorduser.mention}')
            await ctx.send(f'Your turn: {session.turn}')
        if arg == "join":  # for joining created, unstarted game, doesn't work
            pass
        session = getsession(user_id)  # moved to function
            # creategame else should be here?
        if session.in_use:  # might get referenced before assignment ??? checks if session has been started
            if session.turn == user_id:  # checks if player has the turn
                if arg == "self":
                    returned = session.shoot(user_id)
                    await ctx.reply(f"{returned}")
                elif arg == "opponent":
                    target = sr_players[user_id].opponent
                    returned = session.shoot(target)
                    await ctx.reply(f"{returned}")
                if not session.in_use:  # if session is ended check who won and end session properly
                    winner = session.whowins()
                    try:
                        users[winner].givemoney(session.pool)
                    except KeyError:
                        print(f"Tried to give dealer money? {winner} keyerror")
                    session.end(user_id)
                    await ctx.reply(f"**{winner} WINS**")
                if session.in_use and session.turn in dealers:  # if playing against dealer, let him play (while)
                    player = dealers[session.turn]
                    returned = await player.dealerplay(session, ctx)
                    await ctx.reply(f"{returned}")
            else:
                await ctx.reply("Not your turn")
        else:
            await ctx.reply("Game not started, use `!playshotgun start` to start")
    else:
        await ctx.reply("idź na #kasyno-evilpyzy")
        return


@bot.command()
async def bet(ctx, game='', amount=20):
    user_id = ctx.author.id
    if ctx.channel.id in (KASYNO, CHANNEL_ID):  # only allowed to play on correct channel
        if not game:
            await ctx.reply(f"No bet game name provided, correct use !bet shotgun [amount](optional, defaults to 20)")
            return
        if amount < 0:
            await ctx.reply(f"can't bet negative")
            return
        elif game == "shotgun":
            session = getsession(user_id)
            if session and not session.in_use:
                user_id = ctx.author.id
                amount = users[user_id].takemoney(int(amount))
                print(amount)
                print(users[user_id])
                print(users[user_id].money)
                if amount:
                    session.pool += amount
                    pass
                else:
                    await ctx.reply(f"Not enough money")
                    return
            else:
                await ctx.reply(f"{user_id} is not waiting for game to start")
        else:
            await ctx.reply(f"unknown game")

''' for debugging dealerlist
@bot.command()
async def printdealers(ctx):
    await ctx.reply(f"{dealers}")'''