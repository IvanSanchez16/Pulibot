from Actions.Message import send_message, send_embed
from Models.google_api import get_URL
from Models.spotify import get_playlist_tracks,get_album_tracks
from Actions.Music import add_queue, clear_queue, shuffle_queue, add_queue_pl, see_queue, set_three_songs_data, delete_message
import re

regex_sp_pl_url = r'\b(?:https://open.spotify.com/)(?:playlist/|album/)[A-Za-z0-9?]+(?:si=)[A-Za-z0-9]+'


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

    # Puede proporcionar una playlist publica de spotify, el link de yt directamente
    # o poner texto el cual sería como ponerlo en el buscador
    if re.match(regex_sp_pl_url, params[0]):
        url = params[0]
        char = url[25]
        if char == 'p':
            await play_spotify_pl(client, url[34:56])
            return
        await play_spotify_al(client, url[31:53])
        return
    query = ''
    for p in params:
        query = query + ' ' + p
    query = query.strip()

    await add_queue(query, client)
    await ctx.message.add_reaction('▶')


async def play_spotify_pl(client, playlist_id):
    playlist = get_playlist_tracks(playlist_id)
    tracks = playlist['tracks']['items']
    song = tracks[0]['track']
    artistas = ''
    for a in song['artists']:
        artistas += a['name'] + ' '
    artistas = artistas.strip()
    query = f"{song['name']} {artistas}"
    await add_queue_pl(query, client)
    await send_embed(channel='comandos', color=(44, 211, 36), client=client,
                     description=f"{len(tracks)} canciones añadidas a la cola. Playlist: {playlist['name']}")
    tracks.pop(0)
    for song in tracks:
        song = song['track']
        artistas = ''
        for a in song['artists']:
            artistas += a['name'] + ' '
        artistas = artistas.strip()
        query = f"{song['name']} {artistas}"
        await add_queue_pl(query, client)


async def play_spotify_al(client, album_id):
    album = get_album_tracks(album_id)
    tracks = album['tracks']
    song = tracks[0]
    await add_queue_pl(song, client)
    await send_embed(channel='comandos', color=(44, 211, 36), client=client,
                     description=f"{len(tracks)} canciones añadidas a la cola. Album: {album['name']}")
    tracks.pop(0)
    for song in tracks:
        await add_queue_pl(song, client)


async def skip_song(ctx):
    await delete_message()
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


async def set_data_songs():
    await set_three_songs_data()


async def send_queue(client):
    await see_queue()
