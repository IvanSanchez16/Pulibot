import discord


async def send_message(channel='General', message='', client=None):
    if client is None:
        return False
    channels = client.guilds[0].text_channels
    text_channel = discord.utils.get(channels, name=channel)
    if text_channel is None:
        return False
    await text_channel.send(message)
    return True
