import discord
import asyncio
import tweepy
from datetime import datetime, date, time, timedelta
from discord.utils import get

RECORDS_BACKUP_CHANNEL = 912679967228297256
VERIFICATION_CHANNEL = 910138431986876429
COUNTDOWN_CHANNEL = 912406038983098429
TWITTER_CHANNEL = 916032439908982794
FOLLOWERS_TARGET_MESSAGE = 916036295187382292
PASSWORD_MESSAGE = 913691965311291413
KEYHOLDER_PASSWORD_MESSAGE = 913692784249143297
TARGET_DATE_MESSAGE = 913692835604217927
VERIFIED_ROLE = 910216582033199114
KEYHOLDER_ROLE = 912695112520323082
QUEUE_ROLE = 910216738602356736
CONSUMER_KEY = '1IMTDBvzpoqYHbHMWx6evm9nw'
CONSUMER_SECRET = 'iVCwcXcZosDeLnbq88ivceuaw1rdW0OgvUsiYvtrUjjFFy4zeS'
ACCESS_KEY = '1466399636709511170-QbmXh6ya6ZDl9q7yFvEpMacJZH6GjY'
ACCESS_SECRET = 'j4UHJ49PF1ALx7pIgCGafDNA8QmFiqY9HWmFrjQVW6PSe'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAKjaWQEAAAAAjMRm99enygWKiN8hnLCFBOhBtYE%3DRYiBALM9Oc0ktonAnIORnhaAx0aLceW5x5oHf0f2MdL8PPysvU'
ACCOUNT_ID = '1455646119539712000'
WHEN = (datetime.combine(date.today(), time(0, 0, 0)) + timedelta(hours=-5, minutes=-30)).time()

TOKEN = ''

bot = discord.Client()


@bot.event
async def on_ready():
    print('Started')


async def called_once_a_day():
    await bot.wait_until_ready()
    cnt = await bot.get_channel(RECORDS_BACKUP_CHANNEL).fetch_message(TARGET_DATE_MESSAGE)
    dt = cnt.content.split()
    end = datetime(int(dt[-3]), int(dt[-2]), int(dt[-1]))
    today = datetime.today()
    await bot.get_channel(COUNTDOWN_CHANNEL).edit(name=str((end - today).days) + ' days remaining!')

    client = tweepy.Client(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token=ACCESS_KEY, access_token_secret=ACCESS_SECRET, bearer_token=BEARER_TOKEN)
    followers_list = client.get_users_followers(ACCOUNT_ID)
    followers = followers_list.meta['result_count']
    target_cnt = await bot.get_channel(RECORDS_BACKUP_CHANNEL).fetch_message(FOLLOWERS_TARGET_MESSAGE)
    target = int(target_cnt.content.split()[-1])
    await bot.get_channel(TWITTER_CHANNEL).edit(name=str(target - followers) + ' followers more!')


async def background_task():
    now = datetime.utcnow()
    if now.time() > WHEN:
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()
        await asyncio.sleep(seconds)
    while True:
        now = datetime.utcnow()
        target_time = datetime.combine(now.date(), WHEN)
        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)
        await called_once_a_day()
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()
        await asyncio.sleep(seconds)


@bot.event
async def on_message(message):
    pswd = await bot.get_channel(RECORDS_BACKUP_CHANNEL).fetch_message(PASSWORD_MESSAGE)
    pswd = pswd.content.split()[-1]
    key = await bot.get_channel(RECORDS_BACKUP_CHANNEL).fetch_message(KEYHOLDER_PASSWORD_MESSAGE)
    key = key.content.split()[-1]
    if message.content.startswith('!pswd') and message.channel.id == VERIFICATION_CHANNEL:
        if message.content.split()[-1] == pswd:
            member = message.author
            role = get(member.guild.roles, id=VERIFIED_ROLE)
            role2 = get(member.guild.roles, id=QUEUE_ROLE)
            await member.add_roles(role)
            await member.remove_roles(role2)
            embedparam = discord.Embed(title='You are verified now', color=0x0add1f)
            await message.channel.send(embed=embedparam)
            await message.delete()
        elif message.content.split()[-1] == key:
            member = message.author
            role = get(member.guild.roles, id=VERIFIED_ROLE)
            role2 = get(member.guild.roles, id=KEYHOLDER_ROLE)
            role3 = get(member.guild.roles, id=QUEUE_ROLE)
            await member.add_roles(role, role2)
            await member.remove_roles(role3)
            embedparam = discord.Embed(title='You are verified & keyholder now', color=0x0add1f)
            await message.channel.send(embed=embedparam)
            await message.delete()
        else:
            member = message.author
            role = get(member.guild.roles, id=QUEUE_ROLE)
            role2 = get(member.guild.roles, id=VERIFIED_ROLE)
            await member.add_roles(role)
            await member.remove_roles(role2)
            embedparam = discord.Embed(title='Wrong password!!', color=0xff1e00)
            await message.channel.send(embed=embedparam)
            await message.delete()
    elif pswd in message.content or key in message.content:
        await message.delete()
        embedparam = discord.Embed(title='Message deleted', description='Password found in message', color=0x0add1f)
        await message.channel.send(embed=embedparam)


bot.loop.create_task(background_task())
bot.run(TOKEN)
