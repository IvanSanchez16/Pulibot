import discord
import youtube_dl

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


# Obtiene el AudioSource desde una url de Youtube
async def from_url(url):
    info = ytdl.extract_info(url, download=False)
    URL = info['formats'][0]['url']
    player = discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS)
    player = discord.PCMVolumeTransformer(player, 0.5)
    return {
        'player': player,
        'title': info['title'],
        'duration': info['duration'],
        'image': info['thumbnail']
    }
