from utils import days_until_birthday, days_until_birthday_reversed
from datetime import date, timedelta


async def get_last(guild, message, birthdays):
    # Counts the number of days until everyone's birthday individually to find the highest count
    cur_count = 0
    highest_day = 0
    for birthday in birthdays:
        cur_count = days_until_birthday(birthday[1], birthdays)
        if cur_count > highest_day and cur_count != 0:
            highest_day = cur_count

    # Now sends a message for every birthday on the highest day
    highest_day_as_date = str(date.today() + timedelta(days=highest_day))
    highest_day_as_date = highest_day_as_date[5:7] + \
        '/' + highest_day_as_date[8:10]

    for birthday in birthdays:
        if birthday[0] == highest_day_as_date:
            user = guild.get_member(birthday[1])
            await message.channel.send(f'{user.name}\'s birthday is next, which was {days_until_birthday_reversed(birthday[1], birthdays)} days ago on {highest_day_as_date}')
