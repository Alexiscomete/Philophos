import discord, TenGiphPy
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def gif(self, ctx, *, keyword):
        await ctx.message.delete()
        async with ctx.channel.typing():
            rgif = TenGiphPy.Tenor(token='88JQLKP3WXAI')
            msg = rgif.random(keyword)
            embed = discord.Embed()
            embed.add_field(name=f"GIF de **{keyword}** demandé par {ctx.author.name} !", value=ctx.author.mention, inline=False)
            embed.set_image(url=msg)
            embed.set_footer(text=f"Service utilisé : Tenor")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("gif")