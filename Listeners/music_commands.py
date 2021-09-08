from Actions.Message import send_message
from Models.google_api import get_URL
from Actions.Music import add_queue, clear_queue, shuffle_queue


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
