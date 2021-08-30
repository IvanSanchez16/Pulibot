import discord


async def send_message(channel='General', message='', client=None):
    channels = client.guilds[0].text_channels
    text_channel = discord.utils.get(channels, name=channel)
    await text_channel.send(message)
