from googleapiclient.discovery import build
from decouple import config

KEY = config('GOOGLE_KEY')


# Obtener url de un video de yt con el titulo
def get_URL(title):
    with build('youtube', 'v3', developerKey=KEY) as service:
        request = service.search().list(maxResults=1, regionCode='mx', part='snippet', q=title, type='video')
        response = request.execute()
        videoID = response['items'][0]['id']['videoId']
        return f'https://youtube.com/watch?v={videoID}'
