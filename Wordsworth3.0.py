"""
Wordsworth - A Discord Bot
Version 3.0

Change log

v3.0 (4/15/2020) [DONE]
- [DONE] Implemented more flexible functionality to the bot's commands
- [DONE] Cleaned up code to be more legible
- [DONE] Implement a "read your fortune" function (.fortune)
- [DONE] Implement a "roll a dice" function (example - !d6 -> random number between 1 and 6, indicate crits)
- [DONE] Read in poetry, jokes, and status updates from a file

The big goal that spurred creating version 3.0 was to create a more user-friendly and fun version of the bot.
That namely comes in the form of commands that can be accessed via messages rather than just the command prefix.
This was done by creating if/else statements that check messages in the Discord chat to see if they are key phrases.
If so, the event handler for messages will call the necessary command and pass the necessary Context object.
"""


# Imports --------------------------------------------------------------------------------------------------------------
import discord
import random
import time
from discord.ext import commands
from datetime import datetime
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
    elif message.content.lower() == 'tell me the time, wordsworth':
        ctx = await client.get_context(message)
        await time(ctx)
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
    await client.process_commands(message)
# --------------------------------------------------------------------------------------------------------------------//


# Command handling -----------------------------------------------------------------------------------------------------
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! Your ping is currently {round(client.latency * 1000)} ms')


@client.command(aliases=["8ball"])
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
@client.command()
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


@client.command()
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


@client.command()
async def time(ctx):
    t = datetime.now()
    await ctx.send(t)


@client.command()
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


@client.command()
async def poetry(ctx):
    file_chosen = "poem1.txt"
    poem_chosen = random.randrange(1, 4)
    if poem_chosen == 1:
        file_chosen = 'poem1.txt'
    elif poem_chosen == 2:
        file_chosen = 'poem2.txt'
    elif poem_chosen == 3:
        file_chosen = 'poem3.txt'
    file = open(file_chosen, 'r')
    poem = ""
    for line in file:
        poem += line
    file.close()
    await ctx.send(poem)


@client.command()
async def d4(ctx):
    roll = random.randrange(1, 5)
    await ctx.send(roll)


@client.command()
async def d6(ctx):
    roll = random.randrange(1, 7)
    await ctx.send(roll)


@client.command()
async def d10(ctx):
    roll = random.randrange(1, 11)
    await ctx.send(roll)


@client.command()
async def d12(ctx):
    roll = random.randrange(1, 13)
    await ctx.send(roll)


@client.command()
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


@client.command()
async def percentile(ctx):
    roll = random.randrange(1, 101)
    await ctx.send(roll)
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
# Please note that for security reasons, the token has been removed from the public-facing copy of this code
client.run('BotTokenHere')
# --------------------------------------------------------------------------------------------------------------------//
