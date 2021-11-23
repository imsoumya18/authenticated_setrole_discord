import discord
from discord.utils import get

RECORDS_BACKUP_CHANNEL = 912679967228297256
VERIFICATION_CHANNEL = 910138431986876429
PASSWORD_MESSAGE = 912689722776780853
KEYHOLDER_PASSWORD_MESSAGE = 912693500104040478

TOKEN = ''

bot = discord.Client()


@bot.event
async def on_ready():
    print('Started')


@bot.event
async def on_message(message):
    pswd = await bot.get_channel(RECORDS_BACKUP_CHANNEL).fetch_message(PASSWORD_MESSAGE)
    pswd = pswd.content.split()[-1]
    key = await bot.get_channel(RECORDS_BACKUP_CHANNEL).fetch_message(KEYHOLDER_PASSWORD_MESSAGE)
    key = key.content.split()[-1]
    if message.content.startswith('!pswd') and message.channel.id == VERIFICATION_CHANNEL:
        if message.content.split()[-1] == pswd:
            member = message.author
            role = get(member.guild.roles, name='verified')
            role2 = get(member.guild.roles, name='unverified')
            await member.add_roles(role)
            await member.remove_roles(role2)
            embedparam = discord.Embed(title='You are verified now', color=0x0add1f)
            await message.channel.send(embed=embedparam)
            await message.delete()
        elif message.content.split()[-1] == key:
            member = message.author
            role = get(member.guild.roles, name='verified')
            role2 = get(member.guild.roles, name='keyholder')
            role3 = get(member.guild.roles, name='unverified')
            await member.add_roles(role, role2)
            await member.remove_roles(role3)
            embedparam = discord.Embed(title='You are verified & keyholder now', color=0x0add1f)
            await message.channel.send(embed=embedparam)
            await message.delete()
        else:
            member = message.author
            role = get(member.guild.roles, name="unverified")
            role2 = get(member.guild.roles, name="verified")
            await member.add_roles(role)
            await member.remove_roles(role2)
            embedparam = discord.Embed(title='Wrong password!!', color=0xff1e00)
            await message.channel.send(embed=embedparam)
            await message.delete()
    elif pswd in message.content or key in message.content:
        await message.delete()
        embedparam = discord.Embed(title='Message deleted', description='Password found in message', color=0x0add1f)
        await message.channel.send(embed=embedparam)


bot.run(TOKEN)
