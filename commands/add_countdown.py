from utils import days_until_birthday, days_until_birthday_reversed


async def countdown(message, guild, birthdays):
    message_list = message.content
    message_list = message_list.split(' ')

    if len(message_list) == 1:
        await message.channel.send('need to specify a user')
        return

    # Getting the ID
    id_ = ''
    for num in message_list[1]:
        if num.isdigit():
            id_ += num
    id_ = int(id_)
    # Getting the birthday string
    the_date = ''
    for birthday in birthdays:
        if id_ == birthday[1]:
            user = guild.get_member(id_)
            the_date = birthday[0]

    await message.channel.send(f'{user.mention}\'s birthday is {days_until_birthday(id_, birthdays)} days away (or {days_until_birthday_reversed(id_, birthdays)} days ago) on {the_date}')
