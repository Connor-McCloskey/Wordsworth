"""
Wordsworth - A Discord Bot
@author Connor McCloskey
"""

# region Imports
import discord
from discord.ext import commands
import random
import json
import os.path
import glob
from enum import Enum
import logging
from datetime import date, datetime, timedelta
# endregion


# region Class Definitions
class Outcome(Enum):
    TIE = 0
    PLAYER_WINS = 1
    BOT_WINS = 2


class RpsChoices(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


class Wordsworth(commands.Bot):
    # region Vars
    ADMIN: str
    TOKEN: str
    DUNGEON_MASTERS: list
    cmd_dict: dict
    b_loaded = False
    # endregion

    # region Class methods
    def rps_update(self, player, result):
        file_path = "player_data//" + player + ".json"
        update_message = "--- Lifetime Scores ---\n"

        if os.path.exists(file_path):
            file = open(file_path, 'r')
            json_data = json.load(file)
            if result == Outcome.PLAYER_WINS:
                player_score = json_data["wins"]
                player_score += 1
                json_data["wins"] = player_score
            elif result == Outcome.BOT_WINS:
                bot_score = json_data["losses"]
                bot_score += 1
                json_data["losses"] = bot_score
            else:
                tie_score = json_data["ties"]
                tie_score += 1
                json_data["ties"] = tie_score
            update_message += (player + ": " + str(json_data["wins"]) + "\n")
            update_message += ("Wordsworth: " + str(json_data["losses"]) + "\n")
            update_message += ("Ties: " + str(json_data["ties"]) + "\n")
            new_data = json.dumps(json_data)

            file.close()

            file = open(file_path, 'w')
            file.write(new_data)
            file.close()
        else:
            file = open(file_path, 'w')
            player_score = 0
            bot_score = 0
            tie_score = 0
            if result == Outcome.PLAYER_WINS:
                player_score += 1
            elif result == Outcome.BOT_WINS:
                bot_score += 1
            else:
                tie_score += 1
            update_message += (player + ": " + str(player_score) + "\n")
            update_message += ("Wordsworth: " + str(bot_score) + "\n")
            update_message += ("Ties: " + str(tie_score) + "\n")
            data = {
                "player": player,
                "wins": player_score,
                "losses": bot_score,
                "ties": tie_score
            }
            json_data = json.dumps(data)
            file.write(json_data)
            file.close()

        return update_message

    # Create commands and populate cmd_dict
    def create_commands(self):

        if hasattr(self, 'cmd_dict'):
            return

        self.cmd_dict = {}

        # region Misc
        @self.command(brief="Allows the bot's admin to shut down the bot.",
                      description="Allows the bot's admin to shut down the bot.")
        async def sleep(ctx):
            if ctx.author.message.author == self.ADMIN:
                await ctx.send("Wordsworth shutting down...")
                await self.close()
            else:
                await ctx.send("You're not my master!")

        # Return messenger's ping
        @self.command(name="ping",
                      brief="Returns your ping.",
                      description='Returns your ping. Alternate command: Tell me my ping, Wordsworth')
        async def ping(ctx):
            await ctx.send(f'Pong! Your ping is currently {round(self.latency * 1000)} ms')
        self.cmd_dict.update({'tell me my ping, wordsworth': ping})

        # Shitpost my book
        @self.command(name="book", brief="Buy my book!", description="BUY MY FRIGGIN' BOOK")
        async def book_recommendations(ctx):
            message = "There's only one book that matters - Rest in Peace by Connor McCloskey: https://amzn.to/35kLY3x"
            await ctx.send(message)
        self.cmd_dict.update({"give me a book recommendation, wordsworth": book_recommendations})
        # endregion

        # region Games
        # Rock, Paper, Scissors
        @self.command(name="rps", brief="Requires you enter rock, paper, or scissors",
                      description="Play Rock, Paper, or Scissors with Wordsworth!")
        async def rps(ctx, *, player_choice):

            try:
                player_select = RpsChoices[player_choice.upper()]
            except:
                await ctx.send("You've made an illegal choice! Bad!")
                return
            bot_select = random.choice(list(RpsChoices))

            # Initialize our result to a default setting
            result = Outcome.TIE

            message = "You chose: " + player_select.name + "\n"
            message += "I chose: " + bot_select.name + "\n"
            msg_player_win = "You win!\n"
            msg_bot_win = "I win!\n"

            if player_select == bot_select:
                message += "We tie! \n"
                result = Outcome.TIE
            elif player_select == RpsChoices.ROCK:
                if bot_select == RpsChoices.PAPER:
                    message += msg_bot_win
                    result = Outcome.BOT_WINS
                if bot_select == RpsChoices.SCISSORS:
                    message += msg_player_win
                    result = Outcome.PLAYER_WINS
            elif player_select == RpsChoices.PAPER:
                if bot_select == RpsChoices.ROCK:
                    message += msg_player_win
                    result = Outcome.PLAYER_WINS
                if bot_select == RpsChoices.SCISSORS:
                    message += msg_bot_win
                    result = Outcome.BOT_WINS
            # Otherwise, player MUST have chosen scissors
            else:
                print("Player chose scissors")
                if bot_select == RpsChoices.PAPER:
                    message += msg_player_win
                    result = Outcome.PLAYER_WINS
                if bot_select == RpsChoices.ROCK:
                    message += msg_bot_win
                    result = Outcome.BOT_WINS

            history = self.rps_update(ctx.message.author.name, result)
            message += history
            await ctx.send(message)

        # Command to return a Magic 8 Ball-style answer. Also requires the user to enter a question,
        # or else it throws an exception.
        @self.command(aliases=["8ball", "8Ball"], brief='Returns Magic 8 Ball-style answer',
                      description='Returns Magic 8 Ball-style answer. Requires a question after the command prompt.')
        async def _8ball(ctx, *, question):
            responses = ["It is certain.",
                         "It is decidedly so.",
                         "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
                         "Most likely.", "Outlook good.",
                         "Yes.", "Signs point to yes.",
                         "Reply hazy, try again.",
                         "Ask again later.",
                         "Better not tell you now.",
                         "Cannot predict now.",
                         "Concentrate and ask again.",
                         "Don't count on it.",
                         "My reply is no.",
                         "My sources say no.",
                         "Outlook not so good.",
                         "Very doubtful.",
                         "Magic 8 Ball says 'fuck no!'"]
            await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
        # endregion

        # region Content Methods
        # Tell a joke
        @self.command(brief='Tells a joke', description='Tells a joke. Alternate command: Tell me a joke, Wordsworth')
        async def joke(ctx):
            file = open("content//jokes.txt", 'r')
            jokes = file.readlines()
            file.close()
            j = random.choice(jokes)
            await ctx.send(j)
        self.cmd_dict.update({'tell me a joke, wordsworth': joke})

        # Give an inspiring quote
        @self.command(brief="Gives you an inspirational quote",
                      description="Gives you an inspirational quote. Alternate command: Inspire me, Wordsworth",
                      aliases=["inspire"])
        async def quote(ctx):
            file = open("content//quotes.txt", 'r')
            quotes = file.readlines()
            file.close()
            q = random.choice(quotes)
            await ctx.send(q)
        self.cmd_dict.update({'inspire me, wordsworth': quote})

        # Give the user's fortune
        @self.command(brief='Returns your fortune...', description="Returns your fortune...")
        async def fortune(ctx):
            file = open('content//fortune.txt', 'r')
            fortunes = file.readlines()
            file.close()
            f = random.choice(fortunes)
            await ctx.send(f)
        self.cmd_dict.update({"tell me my fortune, wordsworth": fortune})

        # Command for getting the fictional "status"
        @self.command(brief='Ask Wordsworth how he is doing!',
                      description='Ask Wordsworth how he is doing! Alternate command: How are you today, Wordsworth?')
        async def status(ctx):
            file = open('content//status.txt', 'r')
            status_list = file.readlines()
            file.close()
            s = random.choice(status_list)
            await ctx.send(s)
        self.cmd_dict.update({'how are you today, wordsworth?': status})

        # Poetry
        @self.command(brief='Wordsworth will recite some poetry',
                      description='Wordsworth will recite some poetry. Alternate command: Recite some poetry for me, Wordsworth')
        async def poetry(ctx):
            poems = glob.glob("content//poems//*.txt")
            p = random.choice(poems)
            file = open(p, 'r')
            lines = file.readlines()
            msg = ""
            for i in lines:
                msg += i
            file.close()
            await ctx.send(msg)
        self.cmd_dict.update({'recite some poetry for me, wordsworth': poetry})

        # Commands for "X days since DnD shenanigans"
        @self.command(aliases=["start_session", "start_shenanigans"],
                      brief="Record playing a DnD session",
                      description="Record playing a DnD session. Alts: start_session, start_shenanigans, OR we're playing dnd, wordsworth")
        async def record_date(ctx):
            if ctx.message.author.name in self.DUNGEON_MASTERS:
                file = open('content//dnd_date.txt', 'a')
                now = date.today().isoformat()
                file.write(now + "\n")
                file.close()
                await ctx.send("Noted. I've recorded the date of the current session.")
            else:
                await ctx.send("Only a dungeon master may record the campaign date!")
        self.cmd_dict.update({'we\'re playing dnd, wordsworth': record_date})

        # Reports the last date the DnD was played
        @self.command(brief="Returns the number of days since the last DnD session",
                      description="Returns the number of days since the last DnD session. Alts: how long has it been since we last played dnd, wordsworth?")
        async def shenanigans(ctx):
            file = open('dnd_date.txt', 'r')
            last_date_recorded = ""
            for line in file:
                stripped_line = line.strip('\n')
                last_date_recorded = stripped_line
            file.close()
            last_date = date.fromisoformat(last_date_recorded)
            current_date = date.today()
            delta = current_date - last_date
            message = "According to my records, it has been " + delta.days.__str__() + " days since the last DnD session."
            await ctx.send(message)
        self.cmd_dict.update({'how long has it been since we last played dnd, wordsworth': shenanigans})
        # endregion

        # region Dice Rolls
        @self.command(brief="Flip a coin!", description="Flips a coin. Alternate command: flip a coin, wordsworth?")
        async def coin_flip(ctx):
            flip = random.randrange(0, 2)
            flip_result = ""
            if flip == 0:
                flip_result += "Heads"
            elif flip == 1:
                flip_result += "Tails"
            await ctx.send(flip_result)
        self.cmd_dict.update({'flip a coin, wordsworth': coin_flip})

        @self.command(brief='Rolls a d4', description='Rolls a d4. Alternate command: Roll a d4, Wordsworth')
        async def d4(ctx):
            roll = random.randrange(1, 5)
            await ctx.send(roll)
        self.cmd_dict.update({'roll a d4, wordsworth': d4})

        @self.command(brief='Rolls a d6', description='Rolls a d6. Alternate command: Roll a d6, Wordsworth')
        async def d6(ctx):
            roll = random.randrange(1, 7)
            await ctx.send(roll)
        self.cmd_dict.update({'roll a d6, wordsworth': d6})

        @self.command(brief='Rolls a d8', description='Rolls a d6. Alternate command: Roll a d6, Wordsworth')
        async def d8(ctx):
            roll = random.randrange(1, 9)
            await ctx.send(roll)
        self.cmd_dict.update({'roll a d8, wordsworth': d8})

        @self.command(brief='Rolls a d10', description="Rolls a d10. Alternate command: Roll a d10, Wordsworth")
        async def d10(ctx):
            roll = random.randrange(1, 11)
            await ctx.send(roll)
        self.cmd_dict.update({'roll a d10, wordsworth': d10})

        @self.command(brief='Rolls a d12', description='Rolls a d12. Alternate command: Roll a d12, Wordsworth')
        async def d12(ctx):
            roll = random.randrange(1, 13)
            await ctx.send(roll)
        self.cmd_dict.update({'roll a d12, wordsworth': d12})

        @self.command(brief='Rolls a d20', description='Rolls a d20. Alternate command: Roll a d20, Wordsworth')
        async def d20(ctx):
            roll = random.randrange(1, 21)
            if roll == 1:
                critical_fail = "1 - Critical Fail!"
                await ctx.send(critical_fail)
            elif roll == 20:
                critical_success = "20 - Critical Success!"
                await ctx.send(critical_success)
            else:
                await ctx.send(roll)
        self.cmd_dict.update({'roll a d20, wordsworth': d20})

        @self.command(brief='Rolls a percentile die',
                      description="Rolls a percentile die. Alternate command: Roll a percentile die, Wordsworth")
        async def percentile(ctx):
            roll = random.randrange(1, 101)
            await ctx.send(roll)
        self.cmd_dict.update({'roll a percentile die, wordsworth': percentile})
        # endregion

        # region Time Commands
        # For all these time commands...
        # Get the current time in Colorado
        # For times in other states/countries...
        # Create a timedelta object, with the hours passed in as the time difference
        # Add the current time plus the timedelta object
        # Format the output and send the message
        # See Python official documentation on how timedelta and datetime classes operate
        @self.command(brief='Returns the time in Colorado',
                      description='Returns the time in Colorado. Alternate command: Tell me the time in Colorado, Wordsworth')
        async def local_time(ctx):
            t = datetime.now()
            formatted_time = t.strftime("It is %A %B %d %Y at %I:%M %p in Colorado, and all is well!")
            await ctx.send(formatted_time)
        self.cmd_dict.update({'tell me the time in colorado, wordsworth': local_time})

        @self.command(brief='Returns the time in California',
                      description='Returns the time in California. Alternate command: Tell me the time in California, Wordsworth')
        async def cali_time(ctx):
            colorado_t = datetime.now()
            cali_hour_difference = -1
            time_difference_class = timedelta(hours=cali_hour_difference)
            cali_t = colorado_t + time_difference_class
            formatted_time = cali_t.strftime("It is %A %B %d %Y at %I:%M %p in California, and all is well!")
            await ctx.send(formatted_time)
        self.cmd_dict.update({'tell me the time in california, wordsworth': cali_time})

        @self.command(brief='Returns the time in Japan',
                      description='Returns the time in Japan. Alternate command: Tell me the time in Japan, Wordsworth')
        async def japan_time(ctx):
            colorado_t = datetime.now()
            japan_difference = 16
            time_difference_class = timedelta(hours=japan_difference)
            j_time = colorado_t + time_difference_class
            formatted_time = j_time.strftime("It is %A %B %d %Y at %I:%M %p in Japan, and all is well!")
            await ctx.send(formatted_time)
        self.cmd_dict.update({'tell me the time in japan, wordsworth': japan_time})

        @self.command(brief='Gabe time...', description='Meanwhile, in Gabeland...')
        async def GabeTime(ctx):
            t = datetime.now()
            gabe_time_delta = -45
            gabe_time_obj = timedelta(minutes=gabe_time_delta)
            gabe_time = t + gabe_time_obj
            f_gabe_time = gabe_time.strftime("It is %A %B %d %Y at %I:%M %p in Gabeland, and all is well!")
            await ctx.send(f_gabe_time)

        # GabeTime, but RANDOM!
        @self.command(brief='Gabe super time...', description='Meanwhile, in Super Gabeland...')
        async def GabeTimeRandom(ctx):
            t = datetime.now()
            gabe_time_delta = random.randrange(-60, 61)
            gabe_time_obj = timedelta(minutes=gabe_time_delta)
            gabe_time = t + gabe_time_obj
            f_gabe_time = gabe_time.strftime("It is %A %B %d %Y at %I:%M %p in Gabeland, and all is well!")
            await ctx.send(f_gabe_time)
        # endregion

    # Load settings
    def load(self):

        if self.b_loaded is True:
            return

        file = open("settings.json", "r")
        settings = json.load(file)
        self.ADMIN = settings['admin']
        self.TOKEN = settings['token']
        self.DUNGEON_MASTERS = settings['dms']
        file.close()
        self.owner_id = self.ADMIN
        self.create_commands()
        self.b_loaded = True
    # endregion

    # region Event Handling
    async def on_ready(self):
        await self.change_presence(status=discord.Status.online, activity=discord.Game('above Tintern Abbey'))
        """
        for server in self.guilds:
            # For debugging...
            if server.name == "Casa de McCloskey":
                for channel in server.channels:
                    if channel.name == "general":
                        await channel.send("Wordsworth, online.")
        """
        print("Bot ready")

    async def on_message(self, message):

        if message.author == self.user:
            return

        ctx = await self.get_context(message)
        msg = message.content.lower()

        # Custom string commands are stored in a dictionary
        # Here, we do a lookup to see if anything needs to be called
        if msg in self.cmd_dict:
            await self.cmd_dict[msg](ctx)

        await self.process_commands(message)

    async def on_member_join(self, member):
        ctx = member.guild.system_channel
        name = member.display_name
        msg = ("A fine day to you, " + name + "! Welcome to the server!")
        await ctx.send(msg)
    # endregion

    # region Error Handling
    async def on_command_error(self, ctx, error):
        print(error)
        await ctx.send("Sorry, I don't understand...")
    # endregion
# endregion


# region Main
def main():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    logger = logging.FileHandler(filename='wordsworth.log', encoding='utf-8', mode='w')

    instance = Wordsworth(command_prefix=('.', 'Wordsworth, '), intents=intents, log_handler=logger)
    instance.load()
    instance.run(instance.TOKEN)


if __name__ == "__main__":
    main()
# endregion
