from Models.DBConnection import members


async def find_member(member):
    result = members.find_one({"user": str(member)})
    return result


async def insert_member(member, loser_name):
    document = {"user": member.id, "loser_name": loser_name}
    members.insert_one(document)

