import discord, random, asyncio
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="roll", description="Lancer un dé !")
    async def _roll(self, ctx):
        bot_message = await ctx.send("J'ai lancé le dé.")
        await asyncio.sleep(1)
        dice_face = random.randint(1, 6)
        await bot_message.edit(content=f"{ctx.author.mention}, c'est la face numéro **{dice_face}** !")

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("roll")