import discord
from main import client

@client.event
async def on_ready():
    print("Ya prendí")

@client.event
async def on_member_join(member):
    print(f'Entro: {member}')



    #await message.channel.send('Hola')