from utils import days_until_birthday, date_format_to_english
import discord


async def countdown(message, guild, birthdays):
    message_list = message.content
    message_list = message_list.split(' ')

    if len(message_list) == 1:
        await message.channel.send('need to specify a user')
        return

    # Getting the ID
    id_ = ''
    for num in message_list[1]:
        if num.isdigit():
            id_ += num
    id_ = int(id_)
    # Getting the birthday string
    the_date = ''
    for birthday in birthdays:
        if id_ == birthday[1]:
            user = guild.get_member(id_)
            the_date = birthday[0]

    # Sending a nice embed
    embed = discord.Embed(title=f'{user.name}\'s birthday', colour=discord.Colour.magenta())

    embed.add_field(name= 'Date: ', value= date_format_to_english(the_date), inline= False)
    embed.add_field(name= 'Days Away: ', value= f'{days_until_birthday(id_, birthdays)} days', inline= True)
    embed.add_field(name= 'Days Ago: ', value= f'{days_until_birthday(id_, birthdays, True)} days', inline= True)

    await message.channel.send(embed=embed)
    #await message.channel.send(f'{user.mention}\'s birthday is {days_until_birthday(id_, birthdays)} days away (or {days_until_birthday(id_, birthdays, True)} days ago) on {date_format_to_english(the_date)}')
