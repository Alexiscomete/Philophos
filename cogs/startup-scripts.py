import discord, asyncio, random, requests, json
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from discord_slash import cog_ext, SlashContext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global uptime_start
        uptime_start = datetime.now()
        await self.bot.change_presence(activity=discord.Game(name="redémarrage..."))
        await asyncio.sleep(3)
        self.status.start()

    @cog_ext.cog_slash(name="ping", description="Afficher la latence et l'uptime du bot !.")
    async def _ping(self, ctx):
        uptime_now = datetime.now()
        t1 = timedelta(days=uptime_start.day, hours=uptime_start.hour, minutes=uptime_start.minute, seconds=uptime_start.second)
        t2 = timedelta(days=uptime_now.day, hours=uptime_now.hour, minutes=uptime_now.minute, seconds=uptime_now.second)
        uptime = t2 - t1
        bot_latency = round(self.bot.latency * 1000)
        embed = discord.Embed(colour = discord.Colour.green())
        embed.add_field(name=':ping_pong: **ping**', value=f'{bot_latency}ms', inline=False)
        embed.add_field(name=':clock8: **uptime**', value=str(uptime).replace('day','jour').replace('days', 'jours'), inline=False)
        await ctx.send(embed=embed)

    @tasks.loop(seconds=600.0)
    async def status(self):
        rdnb = random.randint(1,3)
        if rdnb == 1:
            global_membercount, global_servers = 0, 0
            for guild in self.bot.guilds:
                for member in guild.members:
                    if member.bot == False:
                        global_membercount += 1
                global_servers += 1
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{global_servers} serveurs | {global_membercount} membres"))
        elif rdnb == 2:
            await self.bot.change_presence(activity=discord.Game(name="iso-land.org/amanager"))
        elif rdnb == 3:
            a_file = open("no-move.json", "r")
            json_object_nm = json.load(a_file)
            a_file.close()
            changelog_versions = json_object_nm['changelogs']
            changelog_versions = list(changelog_versions)
            changelog_versions = changelog_versions[-1]
            await self.bot.change_presence(activity=discord.Game(name=f"v{changelog_versions}"))

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("startup-scripts")