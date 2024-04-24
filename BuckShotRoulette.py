import random
import discord
from discord.ext import commands
from Blackjack_and_Hookers import KASYNO, CHANNEL_ID

intents = discord.Intents.default()

intents.reactions = True
intents.members = True
intents.guilds = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)
# Remove the default help command -need to remove it to join 2 bots together
bot.remove_command('help')

SHELLS = ["blank", "live"]
sr_players = {}
sessions = {}


class Player:
    score = 0

    def __init__(self, userid, health, opponent):  # dealerID is 69
        self.id = userid
        self.health = health
        self.opponent = opponent

    def __str__(self):
        return f"{self.id}"


class Shotgun:
    magazine = []
    turn = 69
    in_use = False
    Player2 = 69

    def __init__(self, gameid):
        self.id = gameid
        self.Player1 = gameid

    def start(self, playerid, opponent):
        if not self.in_use:
            self.magazine.clear()
            sr_players.update({playerid: Player(playerid, random.choice(range(2, 4)), opponent)})
            sr_players.update({sr_players[playerid].opponent: Player(sr_players[playerid].opponent,
                                                                     sr_players[playerid].health, playerid)})
            self.Player2 = sr_players[playerid].opponent
            self.in_use = True
            return self.load()
        else:
            return "Already in use"

    def load(self):
        number = random.choice(range(2, 9))
        i = 0
        while i <= number:
            self.magazine.append(random.choice(SHELLS))
            i += 1
        lives = self.magazine.count('live')
        while lives == len(self.magazine) or lives == 0:
            self.magazine[random.choice(range(number))] = 'blank'
            self.magazine[random.choice(range(number))] = 'live'
            lives = self.magazine.count('live')
        mag_content = f"{lives} live shells, {len(self.magazine) - lives} blanks"
        self.turn = self.id
        print(mag_content)
        return mag_content

    def shoot(self, target):
        if self.magazine and self.magazine[0] == "live":
            sr_players[target].health -= 1
            self.magazine.pop(0)
            self.turnswitch()
            if sr_players[target].health == 0:
                self.in_use = False
                return f"***gunshot*** \n**{target} is dead**"
            if not self.magazine:
                loaded = self.load()
                return "***gunshot*** \nYour turn: " + loaded + str(self.turn)
            return "***gunshot*** \nYour turn: " + str(self.turn)
        elif self.magazine and self.magazine[0] == "blank":
            self.magazine.pop(0)
            if target != self.turn:
                self.turnswitch()
            if not self.magazine:
                loaded = self.load()
                return "***gunshot*** \nYour turn: " + loaded + str(self.turn)
            return "*click*\nYour turn: " + str(self.turn)

    def turnswitch(self):
        if self.turn == self.Player1:
            self.turn = self.Player2
        else:
            self.turn = self.Player1
        return self.turn

    def whowins(self):
        if sr_players[self.Player1].health < 1:
            return self.Player2
        elif sr_players[self.Player2].health < 1:
            return self.Player1
        else:
            return False


async def dealerplay(session, ctx):
    target = session.Player1
    while session.in_use and session.turn == 69:
        if session.magazine.count('live') >= session.magazine.count('blank'):
            returned = "Dealer move:\n **YOU**\n" + session.shoot(target)
            await ctx.reply(f"{returned}")

        else:
            if session.magazine[0] == 'live':
                returned = "Dealer move:\n Self:" + session.shoot(69)
                await ctx.reply(f"{returned}", file=discord.File('shotgungifs/dealersuicide.gif'))
            elif not session.magazine:
                session.load()
            else:
                returned = "Dealer move:\n Self:" + session.shoot(69)
                await ctx.reply(f"{returned}")
        if not session.in_use:
            "Game ended"
    return "Dealer turn ended"


if __name__ == "__main__":  # testing
    Player1 = Player(6969, 2)
    sr_players.update({'6969': Player1})


@bot.command()
async def playshotgun(ctx, arg="", user_mention: discord.User = 69):
    user_id = ctx.author.id
    if ctx.channel.id in (KASYNO, CHANNEL_ID):
        pass
        global sessions
        if arg == "create":
            session = Shotgun(user_id)
            if user_id in sessions:
                del sessions[user_id]
                sessions[user_id] = session
            else:
                sessions[user_id] = session
            # await ctx.reply("Game created, use `!playshotgun start <@user>[optional]` to play:\nPlay using `!playshotgun self` and `!playshotgun opponent`")
            await ctx.reply(
                "Game created, use `!playshotgun start <@user>[only singleplayer for now]` to play:\nPlay using `!playshotgun self` and `!playshotgun opponent`")
            return
        if arg == "start":
            if user_id in sessions:
                session = sessions[user_id]
            else:
                await ctx.reply("Game not created, use `!playshotgun create`")
                return
            # split to create and start?
            if sessions[user_id].in_use:
                await ctx.reply("You are already playing")
                return
            target = user_mention
            if target != 69:
                target = target.id
                if target == user_id:
                    target = 69
            returned = session.start(user_id, target)
            await ctx.reply(f"Game ready: \n {returned}\nhealth: {sr_players[user_id].health}", file=discord.File('shotgungifs/The_Dealer_29.gif'))
            # discorduser = await bot.fetch_user(int(session.turn))
            # await ctx.send(f'Your turn: {discorduser.mention}')
            await ctx.send(f'Your turn: {session.turn}')
        if arg == "join":
            pass

        if user_id in sessions:
            session = sessions[user_id]
        elif sr_players[user_id].opponent in sessions:
            session = sessions[sr_players[user_id].opponent]
        if session.in_use:
            if session.turn == user_id:
                if arg == "self":
                    returned = session.shoot(user_id)
                    await ctx.reply(f"{returned}")
                elif arg == "opponent":
                    target = sr_players[user_id].opponent
                    returned = session.shoot(target)
                    await ctx.reply(f"{returned}")
                if not sessions[user_id].in_use:
                    winner = session.whowins()
                    await ctx.reply(f"**{winner} WINS**")
                if session.in_use and session.turn == 69:
                    returned = await dealerplay(session, ctx)
                    await ctx.reply(f"{returned}")
            else:
                await ctx.reply("Not your turn")
        else:
            await ctx.reply("Game not started, use `!playshotgun start` to start")
    else:
        await ctx.reply("idź na #kasyno-evilpyzy")
        return
