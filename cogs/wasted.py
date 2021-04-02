import discord, requests
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="wasted", description="Afficher ta photo de profil, ou celle d'un utilisateur avec un filtre 'disparu' !", options=[
                create_option(
                name="membre",
                description="Choisis un utilisateur",
                option_type=6,
                required=False
                )])
    async def _wasted(self, ctx, membre: discord.Member = None):
        if membre == None:
            membre = ctx.author
        embed = discord.Embed(title=f"{membre.name} est recherché(e)", description=membre.mention)
        member_avatar_url = str(membre.avatar_url).replace('webp','png').replace('?size=1024','?size=4096')
        embed.set_image(url=f'https://some-random-api.ml/canvas/wasted?avatar={member_avatar_url}')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("wasted")