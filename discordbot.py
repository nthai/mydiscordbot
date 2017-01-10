#!/usr/bin/env python

from discord.ext import commands
import discord
import random
import asyncio
import re
import myyoutube
import mypoe

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

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.BadArgument):
        await bot.send_message(ctx.message.channel, 'Exception: BadArgument.')

@bot.command()
async def kocka(dice : int):
    """Random egész szám generátor"""
    try:
        result = str(random.randint(1, dice))
    except Exception:
        await bot.say('Error during command: kocka')
        return
    await bot.say('Dobás ' + str(dice) + ' oldalú kockával: ' + result)

@bot.command(pass_context = True)
async def zene(ctx, *, msg : str):
    """TODO: zene lejátszás"""
    tmp = await bot.say('Searching for Youtube ID...\nYour input is: ' + msg)
    yt_code = myyoutube.get_youtube_code(msg)
    await bot.edit_message(tmp, 'Youtube code: ' + yt_code)

@bot.command()
async def yt(*, msg : str):
    """Youtube link kereső"""
    tmp = await bot.say('Youtube videó keresése: ' + msg + ' . . .')
    try:
        ans = 'https://www.youtube.com/watch?v={0}'.format(myyoutube.search_youtube_video(msg))
    except myyoutube.NoVideoFoundException:
        ans = 'Nem találtam videót.'
    await bot.edit_message(tmp, ans)

@bot.command()
async def poesearch(*, msg : str):
    """PoE Wiki kereső"""
    tmp = await bot.say('Unique item keresése: ' + msg + '. . .')
    try:
        name_list, link_list = mypoe.search_item(msg)
        ans = '\n'.join(['{0}: {1}'.format(name_list[idx], link_list[idx]) for idx in range(len(name_list))])
        print(name_list)
    except mypoe.NoItemFoundException:
        ans = 'Nem találtam itemet.'
    except mypoe.NetworkError:
        ans = 'Hálózati hiba történt.'
    await bot.edit_message(tmp, ans)

with open('token.tk', mode='r') as input:
    token = input.readline().strip()
    bot.run(token)