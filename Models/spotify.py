import spotipy
from spotipy.oauth2 import SpotifyOAuth
from decouple import config

CLIENT_ID = config('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = config('SPOTIPY_CLIENT_SECRET')
REDIRECT_URL = config('SPOTIPY_REDIRECT_URI')

scopes = 'playlist-read-private'

sa = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URL,
                  scope=scopes)
sp = spotipy.Spotify(auth_manager=sa)


def get_playlist_tracks(playlist_id):
    pl = sp.playlist(playlist_id=playlist_id, fields='name,tracks(total)')
    total_tracks = pl['tracks']['total']
    if total_tracks > 100:
        tracks = sp.playlist_items(playlist_id=playlist_id, fields='items(track(name,artists(name)))')
        tracks = tracks['items']
        count_track = 100
        while count_track < total_tracks:
            aux = sp.playlist_items(playlist_id=playlist_id, fields='items(track(name,artists(name)))', offset=count_track)
            aux = aux['items']
            tracks.extend(aux)
            count_track += len(aux)
        return {
            'name': pl['name'],
            'tracks': tracks
        }

    tracks = sp.playlist_items(playlist_id=playlist_id, fields='items(track(name,artists(name)))')
    return {
        'name': pl['name'],
        'tracks': tracks
    }


def get_album_tracks(album_id):
    album = sp.album(album_id=album_id)
    tracks = album['tracks']['items']
    pl = []
    for track in tracks:
        artists = ''
        for a in track['artists']:
            artists += a['name'] + ' '
        artists = artists.strip()
        pl.append(f"{track['name']} {artists}")
    return {
        'name': album['name'],
        'tracks': pl
    }
