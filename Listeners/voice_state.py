from Actions.Message import send_message
from Models.Member import name_changer
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
        # Ya queda alguien solo
        if len(members) - len(bots) == 1:
            loser = [member for member in members if not member.bot]
            loser = loser[0]
            await send_message(channel='general', message=await name_changer(loser), client=client)

        # Borrar channel_data
        if len(members) == 0:
            time.sleep(1)
            channel = [c for c in channels_data if c['id'] == channel.id][0]
            channels_data.remove(channel)

    # Escenario que alguien entra a un canal
    if not member.bot and before.channel != after.channel and after.channel:
        channel = after.channel
        is_registered = len([c for c in channels_data if c['id'] == channel.id]) == 1
        if len(channel.members) > 1 and not is_registered:
            start_time = time.time() - 1630000000
            channels_data.append({'id': channel.id, 'start_time': start_time})


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
        return 3 <= now <= 15  # 9 pm - 9 am en GMT-6
    return False

