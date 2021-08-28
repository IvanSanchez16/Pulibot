import discord
from decouple import config

TOKEN = config('TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print("Ya prendí")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #await message.channel.send('Hola')

client.run(TOKEN)