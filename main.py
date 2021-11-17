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
            print(f'Current password: {curr}')
        with open('backup.json', 'w') as f:
            new = message.content.split()[1]
            data['password'] = new
            print(f'New password: {new}')
            json.dump(data, f)
    if message.content.lower() == 'pswd':
        member = message.author
        role = get(member.guild.roles, name="verified")
        await member.remove_roles(role)


bot.run(TOKEN)
