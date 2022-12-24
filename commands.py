import discord
from datetime import date, timedelta

async def print_help(message):
    embed = discord.Embed(title='Help!',colour=discord.Colour.magenta())

    #embed.set_author(name='Help!')
    embed.add_field(name='!add', value='must mention a user and birthday in the form \'01/01\'-month and then day in that order-that user\'s birthday will be added to the birthday list', inline=False)
    embed.add_field(name='!birth list', value='returns a list of every birthday added', inline=False)
    embed.add_field(name='!countdown', value='must mention a user, returns that user\'s birthday and how many days until their birthday', inline=False)
    embed.add_field(name='!last', value='returns the last birthday(s)', inline=False)
    embed.add_field(name='!next', value='returns the next birthday(s)', inline=False)

    await message.channel.send(embed=embed)

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
    days_in_four_years = 1461 # Checks for leap year specific dates too
    day_acc = date.today()
    day = str(day_acc)
    day = day[5:7] + '/' + day[8:10]
    while day != new_birthday and days_in_four_years != 0:
        day_acc = day_acc + timedelta(days = 1)
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
        event_file.write(birthdays[event][0] + ', ' + str(birthdays[event][1]) + '\n')
    birthdays.sort()

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

async def birth_list(birthdays, guild, message):
    # Making the birthday list
    birthday_list = ''
    for x in range(len(birthdays)):
        user = guild.get_member(birthdays[x][1])
        birthday_list += user.name + ': ' + birthdays[x][0] + '\n'
    await message.channel.send(birthday_list)

async def get_last(guild, message, birthdays):
    # Counts the number of days until everyone's birthday individually to find the highest count
    cur_count = 0
    highest_day = 0
    for birthday in birthdays:
        cur_count = days_until_birthday(birthday[1], birthdays)
        if cur_count > highest_day and cur_count != 0:
            highest_day = cur_count
    
    # Now sends a message for every birthday on the highest day
    highest_day_as_date = str(date.today() + timedelta(days= highest_day))
    highest_day_as_date = highest_day_as_date[5:7] + '/' + highest_day_as_date[8:10]

    for birthday in birthdays:
        if birthday[0] == highest_day_as_date:
            user = guild.get_member(birthday[1])
            await message.channel.send(f'{user.name}\'s birthday is next, which was {days_until_birthday_reversed(birthday[1], birthdays)} days ago on {highest_day_as_date}')

async def get_next(guild, message, birthdays):
    # Counts the number of days until everyone's birthday individually to find the lowest count
    cur_count = 0
    lowest_day = 367
    for birthday in birthdays:
        cur_count = days_until_birthday(birthday[1], birthdays)
        if cur_count < lowest_day and cur_count != 0:
            lowest_day = cur_count
    
    # Now sends a message for every birthday on the lowest day
    lowest_day_as_date = str(date.today() + timedelta(days= lowest_day))
    lowest_day_as_date = lowest_day_as_date[5:7] + '/' + lowest_day_as_date[8:10]

    for birthday in birthdays:
        if birthday[0] == lowest_day_as_date:
            user = guild.get_member(birthday[1])
            await message.channel.send(f'{user.name}\'s birthday is next, which is {days_until_birthday(birthday[1], birthdays)} away on {lowest_day_as_date}')

# How many days until a mentioned person's birthday
def days_until_birthday(user, birthdays):
    days_until = 0
    birthday = ''
    for details in birthdays:
        if details[1] == user:
            birthday = details[0]
    
    day_acc = date.today()
    day = str(day_acc)
    day = day[5:7] + '/' + day[8:10]
    while day != birthday:
        days_until += 1
        day_acc = day_acc + timedelta(days = 1)
        day = str(day_acc)
        day = day[5:7] + '/' + day[8:10]
    
    return days_until

def days_until_birthday_reversed(user, birthdays):
    days_until = 0
    birthday = ''
    for details in birthdays:
        if details[1] == user:
            birthday = details[0]
    
    day_acc = date.today()
    day = str(day_acc)
    day = day[5:7] + '/' + day[8:10]
    while day != birthday:
        days_until += 1
        day_acc = day_acc - timedelta(days = 1)
        day = str(day_acc)
        day = day[5:7] + '/' + day[8:10]
    
    return days_until