import discord, sqlite3
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    guild_ids = [736689848626446396]
    @cog_ext.cog_slash(guild_ids=guild_ids, name="shop", description="Aller dans la boutique !")
    async def _shop(self, ctx):
        await ctx.send("Bientôt disponible :grin:")

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("shop")