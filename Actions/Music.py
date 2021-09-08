from Actions.Message import send_embed
from Models.ytdl import from_url
import asyncio
import random

# Siempre la canción que esta sonando es la posición 0 del array
queue = []
color = (226, 12, 12)


async def add_queue(voice_client, url, client):
    song = await from_url(url)
    title = song['title']
    field = f'[{title}]({url})'

    # No hay nada sonando
    if len(queue) == 0:
        song['url'] = url
        queue.append(song)
        voice_client.play(song['player'], after=lambda e: next_song(e, client, voice_client))
        await send_embed(channel='comandos', duration_on_secs=song['duration'], title='Reproduciendo',
                         image=song['image'], color=color, client=client, description=field)
        return
    # Añade a la cola la canción
    song['url'] = url
    queue.append(song)
    await send_embed(channel='comandos', title=f'Añadido a la cola - Posición: {len(queue) - 1}',
                     image=song['image'], color=color, client=client, description=field)


def next_song(error, client, voice_client):
    # Si la función fue llamada por un error en la reproducción no se ejecutará
    if not error:
        # No hay cola
        if len(queue) == 1:
            queue.pop(0)
            return
        # Hay cola, reproduce la siguiente canción
        if len(queue) > 1:
            queue.pop(0)
            song = queue[0]
            title = song['title']
            url = song['url']
            field = f'[{title}]({url})'
            voice_client.play(song['player'], after=lambda e: next_song(e, client, voice_client))

            # Aquí hice una mexicanada xd, básicamente la función next_song es llamada desde una lambda la cual no
            # admite funciones asíncronas, pero la función send_embed es asíncrona y necesita un await, por lo que
            # volvería la función asíncrona, pero con ayuda de asyncio y unas horas por stackoverflow encontre que
            # puedo asociar la función(coroutine) send_embed al loop que se genera por el objeto client, el cual es
            # básicamente el bot. Y asi evitar que la función next_song sea asíncrona 😎
            asyncio.run_coroutine_threadsafe(
                send_embed(channel='comandos', duration_on_secs=song['duration'], title='Reproduciendo',
                           image=song['image'], color=color, client=client, description=field), client.loop)
    else:
        print(error)


async def clear_queue(client, band):
    if len(queue) <= 1:
        if band:
            await send_embed(channel='comandos', color=color, client=client,
                             description='No hay cola que borrar')
        return
    # Rescato el primer elemento de la cola porque es la canción que esta sonando actualmente
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
        return
    # Rescato el primer elemento de la cola porque es la canción que esta sonando actualmente
    first_song = queue[0]
    queue.pop(0)
    random.shuffle(queue)
    queue.insert(0, first_song)
    await send_embed(channel='comandos', color=color, client=client,
                     description='Cola de reproducción revuelta')
