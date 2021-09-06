from Actions.Message import send_message
from Models.ytdl import YTDLSource


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
    await channel.connect()

    server = ctx.message.guild
    voice_channel = server.voice_client
    url = params[0]

    async with ctx.typing():
        song = await YTDLSource.from_url(url)
        voice_channel.play(song['player'], after=lambda e: print('Player error: %s' % e) if e else None)
        title = song['title']

    await send_message(channel='comandos', message=f'Reproduciendo {title}', client=client,
                       duration_on_secs=song['duration'])

