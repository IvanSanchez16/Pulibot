import discord
from decouple import config
from Listeners.voice_state import voice_state_update

TOKEN = config('TOKEN')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready(): print("Ya prendí")

@client.event
async def on_member_join(member): print(f'Entro: {member}')

@client.event
async def on_voice_state_update(member, before, after): await voice_state_update(member, before, after)

client.run(TOKEN)
