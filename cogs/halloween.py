import discord, TenGiphPy, json
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="halloween", description="Souhaiter halloween avec un membre !", options=[
                create_option(
                name="membre",
                description="Membre de discord avec qui danser.",
                option_type=6,
                required=False
                )])
    async def _halloween(self, ctx, membre: discord.Member = None):
        a_file = open("no-move.json", "r")
        json_object_nm = json.load(a_file)
        a_file.close()
        tengiphpy_api_key = json_object_nm['token']['tengiphpy']
        embed = discord.Embed()
        rgif = TenGiphPy.Tenor(token=tengiphpy_api_key)
        dance_gif = rgif.random("halloween anime")
        if membre == None:
            embed.add_field(name=f"{ctx.author.name} fête halloween !", value=f'{ctx.author.mention}', inline=False)
            embed.set_image(url=dance_gif)
            await ctx.send(embed=embed)
        else:
            if str(membre) == str(ctx.author):
                embed.add_field(name=f"{ctx.author.name} fête halloween tout seul... !?", value=f"{ctx.author.mention}", inline=False)
                embed.set_image(url=dance_gif)
                await ctx.send(embed=embed)
            else:
                embed.add_field(name=f"{ctx.author.name} a fait peur à {membre.name} ! C'est halloween quand même :jack_o_lantern:", value=f'{ctx.author.mention} {membre.mention}', inline=False)
                embed.set_image(url=dance_gif)
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("halloween")