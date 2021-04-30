import discord, requests, json
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="work", description="Récupérer tes crédits quotidiens !")
    async def _work(self, ctx):
        await ctx.send(f"Cette commande n'est pas disponible pour le moment car le système de cooldown n'est pas *encore* disponible avec les commandes Slash.\nMerci de votre compréhension.")

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("work")