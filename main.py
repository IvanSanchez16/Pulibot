import discord
from discord.ext import commands, tasks
from decouple import config
from Listeners.voice_state import voice_state_update
from Listeners.member_join import member_join

TOKEN = config('TOKEN')

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='-', intents=intents)


@client.event
async def on_ready(): print("Ya prendí")


@client.event
async def on_member_join(member): await member_join(member, client)


@client.event
async def on_voice_state_update(member, before, after): await voice_state_update(member, before, after, client)

client.run(TOKEN)
