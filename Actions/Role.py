import discord


async def assign_role(member, role, client):
    role = discord.utils.get(client.guilds[0].roles, name=role)
    await member.add_roles(role)
