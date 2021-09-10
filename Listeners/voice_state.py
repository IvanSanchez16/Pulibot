from Actions.Message import send_message
from Models.Member import name_changer
import time

channels_data = []


async def voice_state_update(member, before, after, client):
    channel = members = None
    if before.channel:
        channel = before.channel
        members = channel.members

    # Sacar al bot cuando quede solo
    if len(client.voice_clients):
        voice_client = client.voice_clients[0]
        if voice_client.channel == channel and len(members) == 1:
            await voice_client.disconnect()

    # Escenario que alguien sale de un canal
    if not member.bot and not after.channel:
        if not await validate_loser(channel.id):
            return

        bots = [member for member in members if member.bot]
        # Ya queda alguien solo
        if len(members) - len(bots) == 1:
            loser = [member for member in members if not member.bot]
            loser = loser[0]
            await send_message(channel='general', message=await name_changer(loser), client=client)
            await send_message(channel='pruebas', message=loser.id, client=client)

        # Borrar channel_data
        if len(members) == 0:
            channel = [c for c in channels_data if c['id'] == channel.id]
            if len(channel) == 0:
                return
            channel = channel[0]
            channels_data.remove(channel)

    # Escenario que alguien entra a un canal
    if not member.bot and before.channel != after.channel and after.channel:
        channel = after.channel
        is_registered = len([c for c in channels_data if c['id'] == channel.id]) == 1
        if len(channel.members) > 1 and not is_registered:
            start_time = time.time() - 1630000000
            channels_data.append({'id': channel.id, 'start_time': start_time})


# Validar si fue momento de un 'pto el ultimo'
async def validate_loser(channel):
    channel_data = [c for c in channels_data if c['id'] == channel]
    if len(channel_data) == 0:
        return False
    channel_data = channel_data[0]
    now = time.time() - 1630000000
    if now - channel_data['start_time'] >= 10800:  # 3 hrs
        time_object = time.gmtime()
        now = int(time.strftime("%H", time_object))
        return 3 <= now <= 15  # 9 pm - 9 am en GMT-6
    return False

