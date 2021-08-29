from main import client

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #message.channel.send(f'Callate {message.author}')