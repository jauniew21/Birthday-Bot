import asyncio
from commands.add_birthday import add_birthday
from commands.add_countdown import countdown
from commands.get_birthday_list import birth_list
from commands.get_next_birthday import get_next
from commands.get_last_birthday import get_last
from commands.set_reminder import set_reminder
from commands.print_help import print_help
from commands.maintain_birth_list import get_birthdays
import datetime
import discord
from datetime import date, datetime, timedelta
from discord.ext import tasks
import random
from urllib.request import urlopen
from secret import GUILD, SECRET
# Discord Bot Basics
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

birthdays = []
FULL_DAY = 86400

def get_cur_time_in_secs():
    # Finds the exact time the bot starts and turns the hours, minutes, and seconds into integers
    today_datetime = str(datetime.now())
    cur_hour = int(today_datetime[11:13])
    cur_min = int(today_datetime[14:16])
    cur_sec = int(today_datetime[17:19])

    # Converts current time into seconds to be able to countdown until midnight
    cur_time_in_secs = (((cur_hour * 60) + (cur_min)) * 60) + cur_sec

    return cur_time_in_secs

# Finds hours, mins, and secs until midnight
until_midnight = FULL_DAY - get_cur_time_in_secs()

# Finds hours, mins, and secs until 8AM
MORNING = 28800

# Keeps track of the last 'Good Morning!' sent with get_morning()
last_morning = ''

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(1050913970204192848)
    await channel.send('Birthday Bot Online!')
    # The daily birthday check at midnight
    if not nightly.is_running():
        await asyncio.sleep(until_midnight)
        nightly.start()
    # The daily morning message at 8 AM
    if not get_morning.is_running():
        await asyncio.sleep(MORNING)
        get_morning.start()


@client.event
async def on_message(message):
    guild = client.get_guild(GUILD)
    birthdays = get_birthdays(guild)

    if message.author == client.user:
        return

    if message.content == ('!help'):
        await print_help(message)

    if message.content.startswith('!add '):
        await add_birthday(message, guild, birthdays)
    
    if message.content == ('!add'):
        await message.channel.send('You\'re missing some parameters, call !help for more information.')

    if message.content == ('!birth list'):
        await birth_list(birthdays, guild, message)

    if message.content.startswith('!countdown'):
        await countdown(message, guild, birthdays)

    if message.content == ('!last'):
        await get_last(guild, message, birthdays)

    if message.content == ('!next'):
        await get_next(guild, message, birthdays)

    if message.content.startswith('!remind '):
        await set_reminder(guild, message)

    if message.content == ('!remind'):
        await message.channel.send('You\'re missing some parameters, call !help for more information.')

    if message.content.startswith('!yesterday'):
        await message.channel.send(get_yesterday())

    if message.content.startswith('!today'):
        await message.channel.send(get_today())

    if message.content.startswith('!tomorrow'):
        await message.channel.send(get_tomorrow())

@tasks.loop(hours=24)
async def nightly():
    channel = client.get_channel(1050882015848824845)

    for birthday in birthdays:
        if birthday[0] == get_today():
            guild = client.get_guild(GUILD)
            user = guild.get_member(birthday[1])
            await channel.send('Happy Birthday ' + user.mention + '!')
        # Wishing Feb 29th birthdays a happy birthday if it is not a leap year
        elif birthday[0] == '02/29' and get_yesterday() == '02/28':
            guild = client.get_guild(GUILD)
            user = guild.get_member(birthday[1])
            await channel.send('Happy (kind of) Birthday ' + user.mention + '!')


def get_today():
    # Gets today based on the time shift at midnight
    today = date.today()
    today = str(today)
    today = today[5:7] + '/' + today[8:10]
    return today


def get_yesterday():
    # Gets yesterday based on the time shift at midnight
    yesterday = date.today() - timedelta(days=1)
    yesterday = str(yesterday)
    yesterday = yesterday[5:7] + '/' + yesterday[8:10]
    return yesterday


def get_tomorrow():
    # Gets tomorrow based on the time shift at midnight
    tomorrow = date.today() + timedelta(days=1)
    tomorrow = str(tomorrow)
    tomorrow = tomorrow[5:7] + '/' + tomorrow[8:10]
    return tomorrow

@tasks.loop(hours=24)
async def get_morning():
    channel = client.get_channel(1050882015848824845)
    global last_morning

    # Randomly selects a 'Good Morning!' from mornings and sends it to the channel
    mornings = ['Good Morning!', 'Bonjour!', '¡Buenos Días!', 'Buongiorno!', 'Guten Morgen!', 
    'Goede Morgen!', '안녕하세요!', 'おはよう！', 'Доброе утро!', '早上好!', 'Jó Reggelt Kívánok!',
    'Добрий ранок!']
    picker = random.randint(0, len(mornings)-1)

    while (mornings[picker] == last_morning):
        picker = random.randint(0, len(mornings)-1)

    # Grabs the Word of the Day from Merriam-Webster
    url = "https://www.merriam-webster.com/word-of-the-day"
    page = urlopen(url)
    html = page.read().decode("utf-8")

    # The word itself is in the <title> portion of the html
    # So the title is webscraped and parsed to only have the word
    title_i = html.find("<title>")
    start_i = title_i + len("<title>")
    end_i = html.find("</title>")
    title = html[start_i:end_i]
    # Next two lines get the word without mentioning Merriam Webster
    # end_of_word = title.index("|")
    # word = title[17:end_of_word-1]
    
    # Now to get the definition nested from the first paragraph in the <p> tag
    def_index = html.find("<p>")
    def_start_index = def_index + len("<p>")
    def_end_index = html.find("</p>")
    definition = html[def_start_index:def_end_index]

    # And remove any HTML tags in the definition
    while "<" in definition:
        open_index = definition.find("<")
        close_index = definition.find(">")
        definition = definition[:open_index] + definition[close_index + 1:]

    definition = "Definition: " + definition
    last_morning = mornings[picker]

    morning_message = mornings[picker] + '\n' + title + '\n' + '\n' + definition
    await channel.send(morning_message)

client.run(SECRET)