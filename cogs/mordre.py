import discord, TenGiphPy, json
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="bite", description="Vouloir mordre quelqu'un !", options=[
                create_option(
                name="membre",
                description="Membre de discord à qui mordre",
                option_type=6,
                required=False
                )])
    async def _bite(self, ctx, membre: discord.Member = None):
        a_file = open("no-move.json", "r")
        json_object_nm = json.load(a_file)
        a_file.close()
        tengiphpy_api_key = json_object_nm['token']['tengiphpy']
        embed = discord.Embed()
        rgif = TenGiphPy.Tenor(token=tengiphpy_api_key)
        dance_gif = rgif.random("bite anime")
        if membre == None:
            embed.add_field(name=f"{ctx.author.name} a été mordu !", value=f'{ctx.author.mention}', inline=False)
            embed.set_image(url=dance_gif)
            await ctx.send(embed=embed)
        else:
            if str(membre) == str(ctx.author):
                embed.add_field(name=f"{ctx.author.name} s'est mordu(e) soi-même... !?", value=f"{ctx.author.mention}", inline=False)
                embed.set_image(url=dance_gif)
                await ctx.send(embed=embed)
            else:
                embed.add_field(name=f"{ctx.author.name} a mordu {membre.name} !", value=f'{ctx.author.mention} {membre.mention}', inline=False)
                embed.set_image(url=dance_gif)
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("bite")