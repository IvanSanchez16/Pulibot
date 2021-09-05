from Actions.Message import send_message


async def message_sent(message, client):
    # Evitar tome en cuenta sus propios mensajes
    if message.author == client.user:
        return

    # Evitar tomar mensajes de otros bots
    if message.author.bot:
        return

    # Filtrar por canales
    channel = message.channel
    if channel.name == 'general':
        await general_channel(message, client)
        return

    if channel.name == 'comandos':
        await commands_channel(message, client)


async def general_channel(message, client):
    # Evitar multimedia
    if len(message.attachments) > 0:
        await message.delete()
        await send_message(channel='general', message='Aquí existe un orden. No envies multimedia aquí',
                           client=client, duration_on_secs=30)
        return

    # Evitar enlaces
    content = message.content
    if content.startswith('https://') or content.startswith('http://'):
        await message.delete()
        await send_message(channel='general', message='Aquí existe un orden. No envies enlaces aquí',
                           client=client, duration_on_secs=30)
        return

    # Evitar comandos
    if await is_command(content):
        await message.delete()
        await send_message(channel='general', message='Aquí existe un orden. No pongas comandos aquí',
                           client=client, duration_on_secs=30)


async def commands_channel(message, client):
    # Evite lo que sea que no sea un comando
    if not await is_command(message.content):
        await message.delete()
        await send_message(channel='comandos',
                           message='Aquí existe un orden. No envies mensajes aquí, solamente comandos',
                           client=client, duration_on_secs=15)
    if message.content == '-prueba':
        await send_message(channel='comandos', message='!p la noche de anoche',
                           client=client)
        await send_message(channel='comandos', message='-p la noche de anoche',
                           client=client)


async def is_command(message):
    if len(message) == 0:
        return True
    first_char = message[0]
    return first_char == '-' or first_char == '!' or first_char == '/' or first_char == '!'
