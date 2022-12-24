from datetime import date, timedelta


async def add_birthday(message, guild, birthdays):
    message_list = message.content
    message_list = message_list.split(' ')

    # Checking if input is valid
    if len(message_list) < 3:
        await message.channel.send('need to input both a user and a date, in that order, with a space between them')
        return

    # Checking if date is valid
    if len(message_list[2]) != 5:
        await message.channel.send('the date needs to be in the format \'01/01\'-month and then day in that order\nalso make sure you are mentioning the user and entering the date in the correct order')
        return

    new_birthday = message_list[2]
    # Checking if the date is real
    days_in_four_years = 1461  # Checks for leap year specific dates too
    day_acc = date.today()
    day = str(day_acc)
    day = day[5:7] + '/' + day[8:10]
    while day != new_birthday and days_in_four_years != 0:
        day_acc = day_acc + timedelta(days=1)
        day = str(day_acc)
        day = day[5:7] + '/' + day[8:10]
        days_in_four_years -= 1

    if days_in_four_years == 0:
        await message.channel.send('I don\'t think that date exists')
        return

    # Checking if ID is valid
    id_ = ''
    for num in message_list[1]:
        if num.isdigit():
            id_ += num

    try:
        id_ = int(id_)
        user = guild.get_member(id_)
    except:
        await message.channel.send('I cannot find that user :(')
        return

    # If user's birthday is already stored
    for birthday in birthdays:
        if birthday[1] == id_:
            await message.channel.send('I think your birthday is already there, silly!')
            return

    # Adding the new birthday to the event file
    await message.channel.send(f'Birth Logged!\nI can\'t wait to wish you Happy Birthday on {new_birthday}, {user.mention}')
    birthdays.append([new_birthday, id_])
    event_file = open('events.txt', 'w').close()
    event_file = open('events.txt', 'a+')

    for event in range(len(birthdays)):
        event_file.write(birthdays[event][0] + ', ' +
                         str(birthdays[event][1]) + '\n')
    birthdays.sort()
