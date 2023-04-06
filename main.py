import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user.name} is now Online!')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith('!kick'):
        if message.author.guild_permissions.kick_members:
            member = message.mentions[0] if message.mentions else None
            if member:
                try:
                    await member.kick(reason='Kicked by {message.author.name}')
                    await message.channel.send(f'Kicked {member.name}#{member.discriminator}')
                except discord.Forbidden:
                    await message.channel.send("I don't have the necessary permissions to kick members.")
            else:
                await message.channel.send('Please mention a valid member to kick.')
        else:
            await message.channel.send("You don't have permission to kick members.")

    if message.content.startswith('!ban'):
        if message.author.guild_permissions.ban_members:
            member = message.mentions[0] if message.mentions else None
            if member:
                try:
                    await member.ban(reason='Banned by {message.author.name}')
                    await message.channel.send(f'Banned {member.name}#{member.discriminator}')
                except discord.Forbidden:
                    await message.channel.send("I don't have the necessary permissions to ban members.")
            else:
                await message.channel.send('Please mention a valid member to ban.')
        else:
            await message.channel.send("You don't have permission to ban members.")

    if message.content.startswith('!unban'):
        if message.author.guild_permissions.ban_members:
            user_id = message.content.split()[1] if len(message.content.split()) > 1 else None
            if user_id:
                try:
                    banned_users = await message.guild.bans()
                    user = discord.utils.get(banned_users, user_id=user_id)
                    await message.guild.unban(user.user)
                    await message.channel.send(f'Unbanned user with ID: {user_id}')
                except discord.Forbidden:
                    await message.channel.send("I don't have the necessary permissions to unban members.")
            else:
                await message.channel.send('Please provide a valid user ID to unban.')
        else:
            await message.channel.send("You don't have permission to unban members.")

bot.run('TOKEN')
