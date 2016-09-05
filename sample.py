from discord.ext import commands
import discord
import random
import asyncio

description = "A Józsiarcúak csatorna dicsőséges botja."

prefix = ['!']
formatter = commands.HelpFormatter(show_check_failure = False)
bot = commands.Bot(command_prefix=prefix, description=description)


client = discord.Client()

@bot.event
async def on_ready():
    print('Logged in as...')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    print('-----')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

@bot.command()
async def kocka(dice : int):
    """Random egész szám generátor"""
    try:
        result = str(random.randint(1, dice))
    except Exception:
        await bot.say('Error during command: kocka')
        return
    await bot.say('Dobás ' + str(dice) + ' oldalú kockával: ' + result)

with open('token.tk', mode='r') as input:
    token = input.readline().strip()
    bot.run(token)