import discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as...')
    print(client.user.name)
    print(client.user.id)
    print('-----')

@client.event
async def on_message(message):
    if(message.content == '!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit = 100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif(message.content == '!whoami'):
        await client.send_message(message.channel, 'You are {}.'.format(message.author))

with open('token.tk', mode='r') as input:
    token = input.readline().strip()
    client.run(token)