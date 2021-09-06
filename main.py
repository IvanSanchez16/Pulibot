import discord
from discord.ext import commands, tasks
from decouple import config
from Listeners.music_commands import play_song
from Listeners.voice_state import voice_state_update
from Listeners.member_join import member_join
from Listeners.messages import message_sent

TOKEN = config('TOKEN')

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='-', intents=intents)


@client.event
async def on_ready(): print('Yatoy')


@client.event
async def on_member_join(member): await member_join(member, client)


@client.event
async def on_voice_state_update(member, before, after): await voice_state_update(member, before, after, client)


@client.event
async def on_message(message):
    await message_sent(message, client)
    await client.process_commands(message)


@client.command(name='play', help='Reproducir una canción')
async def play(ctx, *params):
    await play_song(ctx, params, client)


client.run(TOKEN)
