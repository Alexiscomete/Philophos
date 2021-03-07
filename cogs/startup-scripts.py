import discord, asyncio, random, requests
from discord.ext import commands, tasks
from datetime import datetime, timedelta

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        global uptime_start
        uptime_start = datetime.now()
        await self.client.change_presence(activity=discord.Game(name="REDÉMARRÉ !"))
        await asyncio.sleep(3)
        self.status.start()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False:
            botinfo_aliases = [f"{self.client.command_prefix}botinfo", f"{self.client.command_prefix}ping", f"{self.client.command_prefix}uptime", f"{self.client.command_prefix}bi"]
            if message.content in botinfo_aliases:
                uptime_now = datetime.now()
                t1 = timedelta(days=uptime_start.day, hours=uptime_start.hour, minutes=uptime_start.minute, seconds=uptime_start.second)
                t2 = timedelta(days=uptime_now.day, hours=uptime_now.hour, minutes=uptime_now.minute, seconds=uptime_now.second)
                uptime = t2 - t1
                bot_latency = round(self.client.latency * 1000)
                embed = discord.Embed(colour = discord.Colour.green())
                embed.add_field(name=':ping_pong: **ping**', value=f'{bot_latency}ms', inline=False)
                embed.add_field(name=':clock8: **uptime**', value=str(uptime).replace('day','jour').replace('days', 'jours'), inline=False)
                await message.channel.send(embed=embed)

    @tasks.loop(seconds=600.0)
    async def status(self):
        rdnb = random.randint(1,3)
        if rdnb == 1:
            global_membercount, global_servers = 0, 0
            for guild in self.client.guilds:
                for member in guild.members:
                    if member.bot == False:
                        global_membercount += 1
                global_servers += 1
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{global_servers} serveurs | {global_membercount} membres"))
        elif rdnb == 2:
            await self.client.change_presence(activity=discord.Game(name="iso-land.org/amanager"))
        elif rdnb == 3:
            changelog_versions = requests.get(f"https://iso-land.org/api/amanager/changelog.json").json()
            changelog_versions = list(changelog_versions['changelogs'])
            changelog_versions = changelog_versions[-1]
            await self.client.change_presence(activity=discord.Game(name=f"v{changelog_versions}"))

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("startup-scripts")