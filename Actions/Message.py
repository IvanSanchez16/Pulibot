import discord


async def send_message(channel='general', message='', client=None, duration_on_secs=-1):
    if client is None:
        return False
    channels = client.guilds[0].text_channels
    text_channel = discord.utils.get(channels, name=channel)
    if text_channel is False:
        return False
    await text_channel.send(message) if duration_on_secs == -1 else await text_channel.send(message, delete_after=duration_on_secs)
    return True



