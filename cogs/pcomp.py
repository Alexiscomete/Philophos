import discord, json, random
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="pcomp", description="Envoyer une phrase complexe pour t'amuser !")
    async def _pcomp(self, ctx):
        a_file = open("no-move.json", "r")
        json_object_nm = json.load(a_file)
        a_file.close()
        await ctx.send(random.choice(json_object_nm['pcomp']))

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("pcomp")