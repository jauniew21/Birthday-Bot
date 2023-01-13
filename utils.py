from datetime import date, timedelta


def days_until_birthday(user, birthdays, reversed=False):
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
        day_acc = day_acc + \
            timedelta(days=1) if not reversed else day_acc - timedelta(days=1)
        day = str(day_acc)
        day = day[5:7] + '/' + day[8:10]

    return days_until


def date_format_to_english(date):
    month, day = date.split('/')
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    
    if day[1] == '1' and day != '11':
        day += 'st'
    elif day[1] == '2' and day != '12':
        day += 'nd'
    elif day[1] == '3' and day != '13':
        day += 'rd'
    else:
        day += 'th'
    
    if day[0] == '0':
        day = day.replace('0', '')

    return f"{months[int(month) - 1]} {day}"
