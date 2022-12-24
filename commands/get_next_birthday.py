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

    # Now sends a message for every birthday on the lowest day
    lowest_day_as_date = str(date.today() + timedelta(days=lowest_day))
    lowest_day_as_date = lowest_day_as_date[5:7] + \
        '/' + lowest_day_as_date[8:10]

    user = guild.get_member(found_birthday[1])
    await message.channel.send(f'{user.name}\'s birthday is next, which is {days_until_birthday(found_birthday[1], birthdays)} days away on {date_format_to_english(lowest_day_as_date)}')
