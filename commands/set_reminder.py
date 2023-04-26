import asyncio

# struct: !remind @me 'to ...' in x (<- time)
async def set_reminder(guild, message):
    message_list = message.content
    message_list = message_list.split(' ')

    # Verifying user id
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
    
    # Finding and storing the reminder
    start_content = 2
    end_content = 0
    for i in range(len(message_list)):
        if message_list[i] == 'in':
            end_content = i

    if message_list[start_content] == 'to':
        reminder = ' '.join(message_list[start_content+1:end_content])
    else:
        reminder = ' '.join(message_list[start_content:end_content])

    # Keeping track of the time
    try:
        time_until = int(message_list[end_content+1])
    except:
        await message.channel.send(f'I\'m not sure when to remind {user} :(')

    # units of time, if specified
    try:
        units = message_list[end_content+2][0]
    except:
        units = 's'

    # validating unit of time
    if units != 's' and units != 'm' and units != 'h':
        await message.channel.send(f'I don\'t know that time measurement :(')
        return
    
    await message.channel.send(f'Alright, I\'ll make sure to remind {user.mention} to {reminder} in {time_until}{units}')

    if (units == 's'):
        await asyncio.sleep(time_until)
    elif (units == 'm'):
        await asyncio.sleep(time_until*60)
    elif (units == 'h'):
        await asyncio.sleep(time_until*60*60)

    await message.channel.send(f'Hey, {user.mention}, {reminder}')