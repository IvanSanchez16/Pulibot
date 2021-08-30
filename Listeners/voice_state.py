from Actions.Message import send_message
from Models.Member import find_member
import time

channels_data = []


async def voice_state_update(member, before, after, client):
    # Escenario que alguien sale de un canal
    if not member.bot and not after.channel:
        channel = before.channel
        members = channel.members
        if not await validate_loser(channel.id):
            return
        bots = [member for member in members if member.bot]
        if len(members) - len(bots) == 1:
            loser = [member for member in members if not member.bot]
            loser = loser[0]
            await send_message(channel='pruebas', message=await name_changer(loser), client=client)

        # Borrar channel_data
        if len(members) == 0:
            channel = [c for c in channels_data if c['id'] == channel.id][0]
            channels_data.remove(channel)

    # Escenario que alguien entra a un canal
    if not member.bot and before.channel != after.channel and after.channel:
        channel = after.channel
        is_registered = len([c for c in channels_data if c['id'] == channel.id]) == 1
        if len(channel.members) > 1 and not is_registered:
            start_time = time.time() - 1630000000
            channels_data.append({'id': channel.id, 'start_time': start_time})
            return


async def validate_loser(channel):
    channel_data = [c for c in channels_data if c['id'] == channel]
    channel_data = channel_data
    if len(channel_data) == 0:
        return False
    channel_data = channel_data[0]
    now = time.time() - 1630000000
    if now - channel_data['start_time'] >= 10800:  # 3 hrs
        time_object = time.gmtime()
        now = int(time.strftime("%H", time_object))
        print(now)
        return 3 <= now <= 15  # 9 pm - 9 am en GMT-6
    return False


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
