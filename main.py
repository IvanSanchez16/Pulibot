import discord
from decouple import config

TOKEN = config('TOKEN')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

client.run(TOKEN)
