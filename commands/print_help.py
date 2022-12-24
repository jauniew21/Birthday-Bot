import discord


async def print_help(message):
    embed = discord.Embed(title='Help!', colour=discord.Colour.magenta())

    # embed.set_author(name='Help!')
    embed.add_field(name='!add', value='must mention a user and birthday in the form \'01/01\'-month and then day in that order-that user\'s birthday will be added to the birthday list', inline=False)
    embed.add_field(name='!birth list',
                    value='returns a list of every birthday added', inline=False)
    embed.add_field(name='!countdown',
                    value='must mention a user, returns that user\'s birthday and how many days until their birthday', inline=False)
    embed.add_field(
        name='!last', value='returns the last birthday(s)', inline=False)
    embed.add_field(
        name='!next', value='returns the next birthday(s)', inline=False)

    await message.channel.send(embed=embed)
