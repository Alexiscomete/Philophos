import discord, random, json
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="lenny", description="Envoyer un lenny !")
    async def _lenny(self, ctx):
        a_file = open("no-move.json", "r")
        json_object_nm = json.load(a_file)
        a_file.close()
        await ctx.send(random.choice(json_object_nm['lenny']))

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("lenny")