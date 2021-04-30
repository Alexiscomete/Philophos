import discord, random, asyncio
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="coin", description="Lancer une pièce pour faire un pile ou face !")
    async def _coin(self, ctx):
        bot_message = await ctx.send("J'ai lancé la pièce.")
        await asyncio.sleep(1)
        if random.randint(1, 2) == 1:
            await bot_message.edit(content=f"{ctx.author.mention}, c'est pile !")
        else:
            await bot_message.edit(content=f"{ctx.author.mention}, c'est face !")

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("coin")