from datetime import date, timedelta


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
        day_acc = day_acc + timedelta(days=1)
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
        day_acc = day_acc - timedelta(days=1)
        day = str(day_acc)
        day = day[5:7] + '/' + day[8:10]

    return days_until
