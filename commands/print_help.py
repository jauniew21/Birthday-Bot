import discord


async def print_help(message):
    embed = discord.Embed(title='Help!', colour=discord.Colour.magenta())

    # embed.set_author(name='Help!')
    embed.add_field(name='!add', 
                    value='must mention a user and birthday in the form \'01/01\'-month and then day in that order-that user\'s birthday will be added to the birthday list', inline=False)
    embed.add_field(name='!birth list',
                    value='returns a list of every birthday added', inline=False)
    embed.add_field(name='!countdown',
                    value='must mention a user, returns that user\'s birthday and how many days until their birthday', inline=False)
    embed.add_field(name='!last', 
                    value='returns the last birthday(s)', inline=False)
    embed.add_field(name='!next', 
                    value='returns the next birthday(s)', inline=False)
    embed.add_field(name='!remind',
                    value='must mention a user, a message to send that user, a number indicating the time to send the message, and the unit of time (s, m, or h), example: \'!remind @{user} to cry 😭 in 5 m\'', inline=False)

    await message.channel.send(embed=embed)
