import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="me", description="Imiter une action !", options=[
                create_option(
                name="action",
                description="L'action à faire",
                option_type=3,
                required=True
                )])
    async def _me(self, ctx, action: str):
        if action == None:
            action = "ne fait rien."
        embed = discord.Embed(description=f"{ctx.author.mention}  {action}")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("me")