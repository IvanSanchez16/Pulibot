from Models.DBConnection import members


async def find_member(member):
    result = members.find_one({"user": str(member)})
    return result


async def insert_member(member, loser_name):
    document = {"user": member.id, "loser_name": loser_name}
    members.insert_one(document)


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

