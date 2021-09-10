from Actions.Message import send_embed
from Models.ytdl import from_url
from Models.google_api import get_URL
import asyncio
import random
import re

# Siempre la canción que esta sonando es la posición 0 del array
queue = []
color = (226, 12, 12)
regex_yt_url = r'\b(?:https://www.youtube.com/watch\?v=)[A-Za-z0-9_&=]+'
message = []


# Reproduce la primera canción de la cola
async def play_song(client):
    if len(queue) == 0 or len(client.voice_clients) == 0:
        return
    voice_client = client.voice_clients[0]
    song = queue[0]
    if len(song['data']) == 0:
        song['data'] = await get_data(song['q'])
    field = f"[{song['data']['title']}]({song['data']['url']})"
    voice_client.play(song['data']['player'], after=lambda e: next_song(e, client))
    message.append(await send_embed(channel='comandos', duration_on_secs=song['data']['duration'], title='Reproduciendo',
                                    image=song['data']['image'], color=color, client=client, description=field))


async def get_data(query):
    # Query es un link de yt
    if re.match(regex_yt_url, query):
        data = await from_url(query)
        data['url'] = query
        return data

    # Query es un str común
    url = get_URL(query)
    data = await from_url(url)
    data['url'] = url
    return data


async def add_queue(query, client):
    # No hay nada sonando
    if len(queue) == 0:
        song = {
            'q': query,
            'data': {}
        }
        queue.append(song)
        await play_song(client)
        return
    # Añade a la cola la canción
    song = {
        'q': query,
        'data': await get_data(query)
    }
    field = f"[{song['data']['title']}]({song['data']['url']})"
    queue.append(song)
    await send_embed(channel='comandos', title=f'Añadido a la cola - Posición: {len(queue) - 1}',
                     image=song['data']['image'], color=color, client=client, description=field)


async def add_queue_pl(query, client):
    # No hay nada sonando
    if len(queue) == 0:
        song = {
            'q': query,
            'data': {}
        }
        queue.append(song)
        await play_song(client)
        return
    # Añade a la cola la canción
    song = {
        'q': query,
        'data': {}
    }
    queue.append(song)


def next_song(error, client):
    # Borra el objeto Message de la canción que terminó
    try:
        message.pop(0)
    except IndexError:
        pass
    # Si la función fue llamada por un error en la reproducción no se ejecutará
    if not error:
        # No hay cola
        if len(queue) == 1:
            queue.pop(0)
            return
        # Hay cola, reproduce la siguiente canción
        if len(queue) > 1:
            queue.pop(0)
            # Aquí hice una mexicanada xd, básicamente la función next_song es llamada desde una lambda la cual no
            # admite funciones asíncronas, pero la función play_song es asíncrona y necesita un await, por lo que
            # volvería la función asíncrona, pero con ayuda de asyncio y unas horas por stackoverflow encontre que
            # puedo asociar la función(coroutine) play_song al loop que se genera por el objeto client, el cual es
            # básicamente el bot. Y asi evitar que la función next_song sea asíncrona 😎
            asyncio.run_coroutine_threadsafe(play_song(client), client.loop)
    else:
        print('Error:')
        print(error)


async def delete_message():
    try:
        message_object = message[0]
        await message_object.delete()
    except IndexError:
        pass


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


async def set_three_songs_data():
    # No hay información que obtener
    if len(queue) <= 1:
        return
    cont = 1
    # Solamente toma la información de 3 canciones
    try:
        while cont < 4 and queue[cont]:
            song = queue[cont]
            if len(song['data']) == 0:
                song['data'] = await get_data(song['q'])
            cont += 1
    except IndexError:
        return


async def see_queue():
    for t in queue:
        print(t)
