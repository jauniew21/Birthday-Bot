from datetime import date, timedelta
from utils import days_until_birthday, date_format_to_english


async def get_next(guild, message, birthdays):
    # Counts the number of days until everyone's birthday individually to find the lowest count
    cur_count = 0
    lowest_day = 367
    found_birthday = None

    for birthday in birthdays:
        cur_count = days_until_birthday(birthday[1], birthdays)
        if cur_count >= lowest_day or cur_count == 0:
            continue

        lowest_day = cur_count
        found_birthday = birthday

    lowest_day_as_date = str(date.today() + timedelta(days=lowest_day))
    lowest_day_as_date = lowest_day_as_date[5:7] + \
        '/' + lowest_day_as_date[8:10]
    
    # Prepares a message that contains every user on the next birthday
    births_that_day = []
    full_message = ''

    # Creates a list of users that share the next birthday
    for birthday in birthdays:
        if birthday[0] == found_birthday[0]:
            user = guild.get_member(birthday[1])
            births_that_day.append(user)
    
    # Sends a message to the chat with all the birthdays in the list
    while len(births_that_day) > 1:
        full_message += f'{births_that_day[0].name} & '
        del births_that_day[0]

    await message.channel.send(f'{full_message}{births_that_day[0].name}\'s birthday is next, which is {days_until_birthday(found_birthday[1], birthdays)} days away on {date_format_to_english(lowest_day_as_date)}')

