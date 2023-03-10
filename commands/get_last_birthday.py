from utils import date_format_to_english, days_until_birthday
from datetime import date, timedelta


async def get_last(guild, message, birthdays):
    # Counts the number of days until everyone's birthday individually to find the highest count
    cur_count = 0
    highest_day = 0
    found_birthday = None
    for birthday in birthdays:
        cur_count = days_until_birthday(birthday[1], birthdays)
        if cur_count <= highest_day or cur_count == 0:
            continue

        highest_day = cur_count
        found_birthday = birthday

    # Now sends a message for every birthday on the highest day
    highest_day_as_date = str(date.today() + timedelta(days=highest_day))
    highest_day_as_date = highest_day_as_date[5:7] + \
        '/' + highest_day_as_date[8:10]
    
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

    await message.channel.send(f'{full_message}{births_that_day[0].name}\'s birthday was last, which was {days_until_birthday(found_birthday[1], birthdays, True)} days ago on {date_format_to_english(highest_day_as_date)}')
