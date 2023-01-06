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

    if found_birthday is None:
        await message.channel.send(f'You have no friends, and therefore no birthdays!')
        return

    # Now sends a message for every birthday on the highest day
    highest_day_as_date = str(date.today() + timedelta(days=highest_day))
    highest_day_as_date = highest_day_as_date[5:7] + \
        '/' + highest_day_as_date[8:10]

    user = guild.get_member(birthday[1])
    await message.channel.send(f'{user.name}\'s birthday was last, which was {days_until_birthday(birthday[1], birthdays, True)} days ago on {date_format_to_english(highest_day_as_date)}')
