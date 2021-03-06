import discord, TenGiphPy
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def bite(self, ctx, *, member: discord.Member = None):
        await ctx.message.delete()
        embed = discord.Embed()
        rgif = TenGiphPy.Tenor(token='88JQLKP3WXAI')
        bite_gif = rgif.random("bite anime")
        if member == None:
            embed.add_field(name=f"{ctx.author.name} mord !", value=f'{ctx.author.mention}', inline=False)
            embed.set_image(url=bite_gif)
            await ctx.send(embed=embed)
        else:
            if str(member) == str(ctx.author):
                embed.add_field(name=f"{ctx.author.name} s'est mordu lui·elle-même... !?", value=f"{ctx.author.mention}", inline=False)
                embed.set_image(url=bite_gif)
                await ctx.send(embed=embed)
            else:
                embed.add_field(name=f"{ctx.author.name} a mordu {member.name} !", value=f'{ctx.author.mention} {member.mention}', inline=False)
                embed.set_image(url=bite_gif)
                await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("bite")