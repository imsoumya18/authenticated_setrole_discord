import json
import discord
from discord.utils import get

TOKEN = ''
bot = discord.Client()


@bot.event
async def on_ready():
    print('Started')


@bot.event
async def on_message(message):
    if message.content.startswith('!setpswd'):
        with open('backup.json', 'r') as f:
            data = json.load(f)
            curr = data['password']
        with open('backup.json', 'w') as f:
            new = message.content.split()[1]
            data['password'] = new
            json.dump(data, f)
            embedparam = discord.Embed(title='Password updated', color=0x0addd7)
            embedparam.add_field(name='New Password:', value=new)
            await message.channel.send(embed=embedparam)
            await message.delete()
    if message.content.startswith('!pswd'):
        pswd = message.content.split()[1]
        with open('backup.json', 'r') as f:
            data = json.load(f)
        if pswd == data['password']:
            member = message.author
            role = get(member.guild.roles, name="verified")
            role2 = get(member.guild.roles, name="unverified")
            await member.add_roles(role)
            await member.remove_roles(role2)
            embedparam = discord.Embed(title='You are verified now', color=0x0add1f)
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


bot.run(TOKEN)
