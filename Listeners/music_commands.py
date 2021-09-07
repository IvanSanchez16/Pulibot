from Actions.Message import send_message
from Models.google_api import get_URL
from Actions.Music import add_queue, next_song


async def play_song(ctx, params, client):
    channel = ctx.channel
    if channel.name != 'comandos':
        return

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

    title = ''
    for p in params:
        title = title + ' ' + p
    url = get_URL(title)

    await add_queue(voice_client, url, client)


async def skip_song(ctx, client):
    voice_client = ctx.message.guild.voice_client
    voice_client.stop()
