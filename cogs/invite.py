import discord, requests
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="invite", description="Afficher les différents liens d'invitation !")
    async def _invite(self, ctx):
        embed = discord.Embed(title="Liens d'invitations")
        embed.add_field(name="Si vous n'avez pas invité le bot sur votre serveur", value="[clique ici](https://iso-land.org/amanager)", inline=False)
        embed.add_field(name="Si vous avez invité le bot avant le 26 mars 2021", value="[clique ici](https://iso-land.org/amanager-add_slash_commands)", inline=False)
        embed.add_field(name="Le serveur support", value="[clique ici](https://discord.gg/WamZS7CExw)", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("invite")