import discord
import random
from Actions.Role import assign_role
from Actions.Message import send_message


async def member_join(member, client):
    await assign_role(member=member, role='Ingainvitados', client=client)
    message = await generate_message(member.id)
    await send_message(channel='pruebas', message=message, client=client)


async def generate_message(member):
    greetings = [
        f'Ese <@!{member}>, como andamos. Bienvenido',
        f'Bienvenido al server <@!{member}>',
        f'Llegó <@!{member}> al server, salúdenlo'
    ]
    return random.choice(greetings)
