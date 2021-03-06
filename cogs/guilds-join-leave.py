import discord
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client
    # A chaque fois que le bot rejoint un serveur
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.client.get_channel(764181117636444230) # In "news-bot" channel
        embed = discord.Embed(title=f"J'ai rejoint un serveur ! :D", description=guild.name)
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text=f"ID : {guild.id}")
        embed.add_field(name="Propriétaire du serveur", value=guild.owner.name, inline=True)
        embed.add_field(name="Nombre d'utilisateurs", value=sum(not member.bot for member in guild.members), inline=True)
        await channel.send(embed=embed)

    # A chaque fois que le bot quitte un serveur
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.client.get_channel(764181117636444230) # In "news-bot" channel
        embed = discord.Embed(title=f"J'ai quitté un serveur... :(", description=guild.name)
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text=f"ID : {guild.id}")
        embed.add_field(name="Propriétaire du serveur", value=guild.owner.name, inline=True)
        embed.add_field(name="Nombre d'utilisateurs", value=sum(not member.bot for member in guild.members), inline=True)
        await channel.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("guilds-join-leave")