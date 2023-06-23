# puts all burthdays into a list, remove ones no longer on the server
def get_birthdays(guild):
    event_file = open('events.txt', 'r')
    content = event_file.readlines()
    birthdays = []

    # Filling Birthdays
    for line in range(len(content)):
        birthdays.append(content[line].strip().split(', '))

    for x in range(len(birthdays)):
        birthdays[x][1] = int(birthdays[x][1])
        if (not guild.get_member(birthdays[x][1])):
            birthdays[x][1] = 'depricated'

    event_file.close()
    birthdays.sort()
    check_users(birthdays)

    return birthdays

def check_users(birthdays):
    event_file = open('events.txt', 'w')

    for event in range(len(birthdays)):
        if (birthdays[event][1] != 'depricated'):
            event_file.write(birthdays[event][0] + ', ' +
                         str(birthdays[event][1]) + '\n')
    
    event_file.close()