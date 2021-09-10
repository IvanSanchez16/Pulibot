import discord
from discord import Colour


async def send_message(channel='general', message='', client=None, duration_on_secs=-1):
    if client is None:
        return False
    channels = client.guilds[0].text_channels
    text_channel = discord.utils.get(channels, name=channel)
    if text_channel is False:
        return False
    return await text_channel.send(message) if duration_on_secs == -1 else await text_channel.send(message, delete_after=duration_on_secs)


async def send_embed(channel='general', duration_on_secs=-1, title='', image='', color=None, description='',
                     footer='', client=None, fields=None):
    if fields is None:
        fields = []
    if color is None:
        color = (0, 0, 0)
    embed = discord.Embed()
    if title != '':
        embed.title = title
    embed.description = description
    embed.colour = Colour.from_rgb(color[0], color[1], color[2])
    if image != '':
        embed.set_thumbnail(url=image)
    if footer != '':
        embed.set_footer(text=footer)

    for field in fields:
        embed.add_field(name=field[0], value=field[1])

    channels = client.guilds[0].text_channels
    text_channel = discord.utils.get(channels, name=channel)
    if text_channel is False:
        return False

    return await text_channel.send(embed=embed) if duration_on_secs == -1 else await text_channel.send(embed=embed, delete_after=duration_on_secs)


