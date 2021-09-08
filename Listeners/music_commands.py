from Actions.Message import send_message
from Models.google_api import get_URL
from Actions.Music import add_queue, clear_queue, shuffle_queue
import re

regex_yt_url = r'\b(?:https://youtube.com/watch?v=)[A-Za-z0-9-_&=]+'


async def play_song(ctx, params, client):
    channel = ctx.message.author.voice
    if not channel:
        await send_message(channel='comandos', message='No estás conectado a ningún canal de voz',
                           client=client)
        return

    channel = channel.channel
    if len(client.voice_clients) != 0:
        if channel != client.voice_clients[0].channel:
            await send_message(channel='comandos', message='Ya estoy ocupado en otro canal',
                               client=client)
            return
    else:
        await channel.connect()

    server = ctx.message.guild
    voice_client = server.voice_client

    # Puede proporcionar el link de yt directamente o poner texto el cual sería como ponerlo en el buscador
    title = ''
    if re.match(regex_yt_url, params[0]):
        url = params[0]
    else:
        for p in params:
            title = title + ' ' + p
        url = get_URL(title)  # Obtiene la url del primer video de yt encontrado con lo escrito

    await add_queue(voice_client, url, client)
    await ctx.message.add_reaction('▶')


async def skip_song(ctx):
    voice_client = ctx.message.guild.voice_client
    voice_client.stop()
    await ctx.message.add_reaction('⏭')


async def clear_q(ctx, client):
    await clear_queue(client, True)
    await ctx.message.add_reaction('🗑️')


async def shuffle_q(ctx, client):
    await shuffle_queue(client)
    await ctx.message.add_reaction('🔀')


async def leave_channel(ctx, client):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()
    await clear_queue(client, False)
    await ctx.message.add_reaction('👋')
