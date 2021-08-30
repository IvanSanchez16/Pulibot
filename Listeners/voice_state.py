import discord


async def voice_state_update(member, before, after):
    if not after.channel and not member.bot:
        channel = before.channel
        members = channel.members
        bots = [member for member in members if member.bot]
        if len(members) - len(bots) == 1:
            looser = [member for member in members if not member.bot]
            looser = looser[0]
            print(looser)

    elif not member.bot:
        channel = after.channel
        await channel.connect()
