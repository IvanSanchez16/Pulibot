from Actions.Message import send_embed
from Models.ytdl import YTDLSource
import asyncio
import random

queue = []
color = (226, 12, 12)


async def add_queue(voice_client, url, client):
    song = await YTDLSource.from_url(url)
    title = song['title']
    field = f'[{title}]({url})'

    if len(queue) == 0:
        song['url'] = url
        queue.append(song)
        voice_client.play(song['player'], after=lambda e: next_song(e, client, voice_client))
        await send_embed(channel='comandos', duration_on_secs=song['duration'], title='Reproduciendo',
                         image=song['image'], color=color, client=client, description=field)
        return
    song['url'] = url
    queue.append(song)
    await send_embed(channel='comandos', title=f'Añadido a la cola - Posición: {len(queue) - 1}',
                     image=song['image'], color=color, client=client, description=field)


def next_song(error, client, voice_client):
    if not error:
        if len(queue) == 1:
            queue.pop(0)
            return
        if len(queue) > 1:
            queue.pop(0)
            song = queue[0]
            title = song['title']
            url = song['url']
            field = f'[{title}]({url})'
            voice_client.play(song['player'], after=lambda e: next_song(e, client, voice_client))
            asyncio.run_coroutine_threadsafe(
                send_embed(channel='comandos', duration_on_secs=song['duration'], title='Reproduciendo',
                           image=song['image'], color=color, client=client, description=field), client.loop)
    else:
        print(error)


async def clear_queue(client, band):
    if len(queue) <= 1:
        await send_embed(channel='comandos', color=color, client=client,
                         description='No hay cola que borrar')
    first_song = queue[0]
    queue.clear()
    queue.insert(0, first_song)
    if band:
        await send_embed(channel='comandos', color=color, client=client,
                         description='Cola de reproducción borrada')


async def shuffle_queue(client):
    if len(queue) <= 1:
        await send_embed(channel='comandos', color=color, client=client,
                         description='No hay cola que revolver')
    first_song = queue[0]
    queue.pop(0)
    random.shuffle(queue)
    queue.insert(0, first_song)
    await send_embed(channel='comandos', color=color, client=client,
                     description='Cola de reproducción revuelta')
