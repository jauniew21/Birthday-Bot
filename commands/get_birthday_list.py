from utils import date_format_to_english


async def birth_list(birthdays, guild, message):
    # Making the birthday list
    birthday_list = ''
    for x in range(len(birthdays)):
        user = guild.get_member(birthdays[x][1])
        birthday_list += user.name + ': ' + \
            date_format_to_english(birthdays[x][0]) + '\n'
    await message.channel.send(birthday_list)
