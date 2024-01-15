import discord
from discord.ext import commands, tasks

class MyBot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        self.recent_mass_pings = []
        self.banned_users = []
        self.check_mass_pings.start()

    @tasks.loop(seconds=2)
    async def check_mass_pings(self):
        for message in self.recent_mass_pings:
            self.recent_mass_pings.remove(message)
            await message.channel.send('**WARNING!** Mass ping detected in this channel.')

    async def on_ready(self):
        print('Bot is ready')

    async def on_message(self, message):
        if message.author.bot:
            return  # Ignore messages from other bots

        if message.content.startswith('@everyone') or message.content.startswith('@here'):
            if len(message.mentions) > 20:
                await message.channel.send('**WARNING!** Mass ping detected in this channel.')
                self.recent_mass_pings.append(message)

    async def on_guild_ban(self, guild, user):
        if user.id not in self.banned_users and len(guild.bans) - len(self.banned_users) > 3:
            await guild.ban(user)
            alert_channel_id = 123456789012345678  # Replace with the actual channel ID
            alert_channel = guild.get_channel(alert_channel_id)
            if alert_channel:
                await alert_channel.send(f'**WARNING!** Mass ban detected in the server. User **@{user.name}** has been banned.')
            await user.send(embed=discord.Embed(title='**You have been banned**', description='You have been banned for attempting a mass ban.', color=discord.Color.red))

            self.banned_users.append(user.id)

bot = MyBot(command_prefix='!')
bot.run('BOT_TOKEN')
