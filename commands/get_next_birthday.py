from datetime import date, timedelta
from utils import days_until_birthday, days_until_birthday_reversed


async def get_next(guild, message, birthdays):
    # Counts the number of days until everyone's birthday individually to find the lowest count
    cur_count = 0
    lowest_day = 367
    for birthday in birthdays:
        cur_count = days_until_birthday(birthday[1], birthdays)
        if cur_count < lowest_day and cur_count != 0:
            lowest_day = cur_count

    # Now sends a message for every birthday on the lowest day
    lowest_day_as_date = str(date.today() + timedelta(days=lowest_day))
    lowest_day_as_date = lowest_day_as_date[5:7] + \
        '/' + lowest_day_as_date[8:10]

    for birthday in birthdays:
        if birthday[0] == lowest_day_as_date:
            user = guild.get_member(birthday[1])
            await message.channel.send(f'{user.name}\'s birthday is next, which is {days_until_birthday(birthday[1], birthdays)} away on {lowest_day_as_date}')
