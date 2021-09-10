import discord
from discord.ext import commands, tasks
from decouple import config
from Listeners.music_commands import play_song, skip_song, clear_q, shuffle_q, leave_channel, send_queue, set_data_songs
from Listeners.voice_state import voice_state_update
from Listeners.member_join import member_join
from Listeners.messages import message_sent

TOKEN = config('TOKEN')

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='-', intents=intents)


# Se definen todos los eventos, comandos, etc. Y se envía el objeto client para poder manipularlo
@client.event
async def on_ready():
    print('Yatoy')
    set_song_data.start()


@client.event
async def on_member_join(member): await member_join(member, client)


@client.event
async def on_voice_state_update(member, before, after): await voice_state_update(member, before, after, client)


@client.event
async def on_message(message):
    await message_sent(message, client)
    await client.process_commands(message)  # Es necesario para que pueda atender los comandos, solamente si tienes
                                            # el evento de on_message


async def is_commands(ctx):
    # Si no viene del canal de comandos se ignora el comando
    channel = ctx.channel
    return channel.name == 'comandos'


@tasks.loop(minutes=5.0)
async def set_song_data():
    await set_data_songs()


@client.command(name='p', help='Reproducir una canción')
async def play(ctx, *params):
    if await is_commands(ctx):
        await play_song(ctx, params, client)


@client.command(name='skip', help='Saltar a la siguiente canción')
async def skip(ctx):
    if await is_commands(ctx):
        await skip_song(ctx)


@client.command(name='clear', help='Limpia la cola de reproducción')
async def clear(ctx):
    if await is_commands(ctx):
        await clear_q(ctx, client)


@client.command(name='leave', help='Desconectar al bot')
async def leave(ctx):
    if await is_commands(ctx):
        await leave_channel(ctx, client)


@client.command(name='shuffle', help='Mezcla la cola de reproducción')
async def shuffle(ctx):
    if await is_commands(ctx):
        await shuffle_q(ctx, client)


@client.command(name='queue', help='Consultar cola de reproducción')
async def queue(ctx):
    if await is_commands(ctx):
        await send_queue(client)

client.run(TOKEN)
