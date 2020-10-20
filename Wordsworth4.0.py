"""
Wordsworth - A Discord Bot
Version 4.0

Change log

v4.0 (10/08/2020) [DONE]
- [DONE] Adding functions to tell time in Colorado vs California vs Japan

v.4.1 (10/09/2020) [DONE]
- [DONE] Add information for help command

v.4.2 (10/15/2020) [DONE]
- [DONE] Added functions to record date of playing a DnD session and returning days since the last session.
"""


# Imports --------------------------------------------------------------------------------------------------------------
import discord
import random
import time
from discord.ext import commands
from datetime import date, datetime, timedelta
# --------------------------------------------------------------------------------------------------------------------//


# Create an instance of a bot and assign it a command prefix------------------------------------------------------------
client = commands.Bot(command_prefix=('.', 'Wordsworth, '))
# --------------------------------------------------------------------------------------------------------------------//


# Event Handling--------------------------------------------------------------------------------------------------------
# Event handler for on_ready event
# Essentially catches event thrown when the bot comes online, sets its status, then prints ready statement to console
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('above Tintern Abbey'))
    print("Bot is ready!")


# Event handler for on_message event
# Reads messages sent to the discord channel and determines if they're intended to be commands
# If so, it calls the corresponding command and passes the necessary Context object
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower() == 'how are you today, wordsworth?':
        ctx = await client.get_context(message)
        await status(ctx)
    elif message.content.lower() == 'tell me my ping, wordsworth':
        ctx = await client.get_context(message)
        await ping(ctx)
    elif message.content.lower() == 'tell me a joke, wordsworth':
        ctx = await client.get_context(message)
        await joke(ctx)
    elif message.content.lower() == 'recite some poetry for me, wordsworth':
        ctx = await client.get_context(message)
        await poetry(ctx)
    elif message.content.lower() == 'tell me the time in colorado, wordsworth':
        ctx = await client.get_context(message)
        await time(ctx)
    elif message.content.lower() == 'tell me the time in california, wordsworth':
        ctx = await client.get_context(message)
        await cali_time(ctx)
    elif message.content.lower() == 'tell me the time in japan, wordsworth':
        ctx = await client.get_context(message)
        await japan_time(ctx)
    elif message.content.lower() == "roll a d4, wordsworth":
        ctx = await client.get_context(message)
        await d4(ctx)
    elif message.content.lower() == "roll a d6, wordsworth":
        ctx = await client.get_context(message)
        await d6(ctx)
    elif message.content.lower() == "roll a d10, wordsworth":
        ctx = await client.get_context(message)
        await d10(ctx)
    elif message.content.lower() == "roll a d12, wordsworth":
        ctx = await client.get_context(message)
        await d12(ctx)
    elif message.content.lower() == "roll a d20, wordsworth":
        ctx = await client.get_context(message)
        await d20(ctx)
    elif message.content.lower() == "roll a percentile die, wordsworth":
        ctx = await client.get_context(message)
        await percentile(ctx)
    elif message.content.lower() == "we're playing dnd, wordsworth":
        ctx = await client.get_context(message)
        await recordDate(ctx)
    elif message.content.lower() == "how long has it been since we last played dnd, wordsworth?":
        ctx = await client.get_context(message)
        await shenanigans(ctx)
    await client.process_commands(message)
# --------------------------------------------------------------------------------------------------------------------//


# Command handling -----------------------------------------------------------------------------------------------------
@client.command(brief='Returns your ping',
                description='Returns your ping. Alternate command: Tell me my ping, Wordsworth')
async def ping(ctx):
    await ctx.send(f'Pong! Your ping is currently {round(client.latency * 1000)} ms')


@client.command(aliases=["8ball", "8Ball"], brief='Returns Magic 8 Ball-style answer',
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


# Remember that the first line in our joke file represents the size of the file (number of jokes available)
# While joke_size w/o + 1 would give us the correct number of jokes, we actually want to increment this since
# randrange's upper bound is non-inclusive. Say we have 14 jokes, and thus the first line in the joke file is 14.
# We add one to this so that joke_size equals 15. We plug this into randrange, which now gives us a random number
# between 1 and 14.
@client.command(brief='Tells a joke', description='Tells a joke. Alternate command: Tell me a joke, Wordsworth')
async def joke(ctx):
    file = open('jokes.txt', 'r')
    joke_size = int(file.readline()) + 1
    joke_chosen = random.randrange(1, joke_size)
    lines_read = 1
    for joke_ in file:
        if lines_read == joke_chosen:
            file.close()
            await ctx.send(joke_)
            break
        lines_read += 1


@client.command(brief='Returns your fortune...', description="Returns your fortune...")
async def fortune(ctx):
    file = open('fortune.txt', 'r')
    fortune_size = int(file.readline()) + 1
    fortune_chosen = random.randrange(1, fortune_size)
    lines_read = 1
    for fortune_ in file:
        if lines_read == fortune_chosen:
            file.close()
            await ctx.send(fortune_)
            break
        lines_read += 1


@client.command(brief='Returns the time in Colorado',
                description='Returns the time in Colorado. Alternate command: Tell me the time in Colorado, Wordsworth')
async def time(ctx):
    t = datetime.now()
    formatted_time = t.strftime("It is %A %B %d %Y at %I:%M %p in Colorado, and all is well!")
    await ctx.send(formatted_time)


@client.command(brief='Ask Wordsworth how he is doing!',
                description='Ask Wordsworth how he is doing! Alternate command: How are you today, Wordsworth?')
async def status(ctx):
    file = open('status.txt', 'r')
    status_size = int(file.readline()) + 1
    status_chosen = random.randrange(1, status_size)
    lines_read = 1
    for status_ in file:
        if lines_read == status_chosen:
            file.close()
            await ctx.send(status_)
            break
        lines_read += 1


@client.command(brief='Wordsworth will recite some poetry',
                description='Wordsworth will recite some poetry. Alternate command: Recite some poetry for me, Wordsworth')
async def poetry(ctx):
    poem_chosen = random.randrange(1, 16)
    p_string = "poem"
    file_type = ".txt"
    p_num = poem_chosen.__str__()
    file_chosen = p_string + p_num + file_type
    file = open(file_chosen, 'r')
    poem = ""
    for line in file:
        poem += line
    file.close()
    await ctx.send(poem)


# Commands for "X days since DnD shenanigans"
@client.command(aliases=["start_session", "start_shenanigans"],
                brief="Record playing a DnD session",
                description="Record playing a DnD session. Alternate commands: start_session, start_shenanigans, OR we're playing dnd, wordsworth")
async def recordDate(ctx):
    file = open('dnd_date.txt', 'a')
    now = date.today().isoformat()
    file.write(now + "\n")
    file.close()
    await ctx.send("Noted. I've recorded the date of the current session.")


@client.command(brief="Returns the number of days since the last DnD session",
                description="Returns the number of days since the last DnD session. Alternate command: how long has it been since we last played dnd, wordsworth?")
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


@client.command(brief='Rolls a d4', description='Rolls a d4. Alternate command: Roll a d4, Wordsworth')
async def d4(ctx):
    roll = random.randrange(1, 5)
    await ctx.send(roll)


@client.command(brief='Rolls a d6', description='Rolls a d6. Alternate command: Roll a d6, Wordsworth')
async def d6(ctx):
    roll = random.randrange(1, 7)
    await ctx.send(roll)


@client.command(brief='Rolls a d10', description="Rolls a d10. Alternate command: Roll a d10, Wordsworth")
async def d10(ctx):
    roll = random.randrange(1, 11)
    await ctx.send(roll)


@client.command(brief='Rolls a d12', description='Rolls a d12. Alternate command: Roll a d12, Wordsworth')
async def d12(ctx):
    roll = random.randrange(1, 13)
    await ctx.send(roll)


@client.command(brief='Rolls a d20', description='Rolls a d20. Alternate command: Roll a d20, Wordsworth')
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


@client.command(brief='Rolls a percentile die',
                description="Rolls a percentile die. Alternate command: Roll a percentile die, Wordsworth")
async def percentile(ctx):
    roll = random.randrange(1, 101)
    await ctx.send(roll)


# For both all these time commands...
# Get the current time in Colorado
# Create a timedelta object, with the hours passed in as the time difference
# Add the current time plus the timedelta object
# Format the output and send the message
# See Python official documentation on how timedelta and datetime classes operate

@client.command(brief='Returns the time in California',
                description='Returns the time in California. Alternate command: Tell me the time in California, Wordsworth')
async def cali_time(ctx):
    colorado_t = datetime.now()
    cali_hour_difference = -1
    time_difference_class = timedelta(hours=cali_hour_difference)
    cali_t = colorado_t + time_difference_class
    formatted_time = cali_t.strftime("It is %A %B %d %Y at %I:%M %p in California, and all is well!")
    await ctx.send(formatted_time)


@client.command(brief='Returns the time in Japan',
                description='Returns the time in Japan. Alternate command: Tell me the time in Japan, Wordsworth')
async def japan_time(ctx):
    colorado_t = datetime.now()
    japan_difference = 15
    time_difference_class = timedelta(hours=japan_difference)
    j_time = colorado_t + time_difference_class
    formatted_time = j_time.strftime("It is %A %B %d %Y at %I:%M %p in Japan, and all is well!")
    await ctx.send(formatted_time)


@client.command(brief='Gabe time...', description='Meanwhile, in Gabeland...')
async def GabeTime(ctx):
    t = datetime.now()
    gabe_time_delta = 45
    gabe_time_obj = timedelta(minutes=gabe_time_delta)
    gabe_time = t + gabe_time_obj
    f_gabe_time = gabe_time.strftime("It is %A %B %d %Y at %I:%M %p in Gabeland, and all is well!")
    await ctx.send(f_gabe_time)
# --------------------------------------------------------------------------------------------------------------------//


# Error checking -------------------------------------------------------------------------------------------------------
@client.event
async def on_command_error(ctx, error):
    print(error)
    await ctx.send("Sorry, I don't understand...")


# For catching 8ball errors
@_8ball.error
async def _8ball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Error. Please input a question.")
# --------------------------------------------------------------------------------------------------------------------//


# Run the bot, passing in the bot token so it knows which application to use -------------------------------------------
client.run('Bot token would go here! Taken down for GitHub security purposes.')
# --------------------------------------------------------------------------------------------------------------------//
