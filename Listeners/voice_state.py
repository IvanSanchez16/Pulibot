from Actions.Message import send_message
from Models.Member import find_member


async def voice_state_update(member, before, after, client):
    if not after.channel and not member.bot:
        channel = before.channel
        members = channel.members
        bots = [member for member in members if member.bot]
        if len(members) - len(bots) == 1:
            loser = [member for member in members if not member.bot]
            loser = loser[0]
            await send_message(channel='pruebas', message=await name_changer(loser), client=client)


async def name_changer(member):
    result = await find_member(member.id)
    if result:
        return result['loser_name']

    name = member.name.lower()
    length = len(name)
    if length <= 4:
        for i in range(0, length):
            ch = name[i]
            if ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u' or ch == 'y':
                return f'put{name[i:length]}'

    j = length - 4
    while j >= 0:
        ch = name[j]
        if ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u' or ch == 'y':
            return f'put{name[j:length]}'
        j = j - 1
    return f'puto el {name}'
