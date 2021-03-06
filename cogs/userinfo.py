import discord
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['ui'])
    async def userinfo(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        roles_list, espace = [], " "
        for role in member.roles:
            if str(role) != "@everyone":
               roles_list.append(str(role.mention))
        embed = discord.Embed(title=str(member.name) + "#" + str(member.discriminator), description=member.mention, color=0xf5900b)
        embed.set_thumbnail(url=str(member.avatar_url))
        embed.set_footer(text=f"ID : {member.id}")
        embed.add_field(name="A rejoint le serveur", value=member.joined_at.strftime("%d/%m/%Y • %H:%M:%S"), inline=True)
        embed.add_field(name="Inscription sur Discord", value=member.created_at.strftime("%d/%m/%Y • %H:%M:%S"), inline=True)
        embed.add_field(name="Liste des rôles", value=espace.join(roles_list), inline=True)
        if member.premium_since != None:
            embed.add_field(name="Abonné à Nitro depuis", value=member.premium_since.strftime("%d/%m/%Y • %H:%M:%S"), inline=True)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("userinfo")