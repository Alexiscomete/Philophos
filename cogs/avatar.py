import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="avatar", description="Afficher ta photo de profil, ou celle d'un utilisateur !", options=[
                create_option(
                name="membre",
                description="Membre de discord à qui souhaiter un anniversaire",
                option_type=6,
                required=False
                )]) 
    async def _avatar(self, ctx, membre: discord.Member = None):
        if membre == None:
            membre = ctx.author
        embed = discord.Embed(title=f"Avatar de {membre.name}", description=membre.mention)
        embed.set_image(url=membre.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("avatar")