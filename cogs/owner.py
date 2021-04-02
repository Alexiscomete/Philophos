import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    guilds_id = [736689848626446396]
    @cog_ext.cog_slash(guilds_id=guilds_id, name="owner", description="⛔ Commande autorisée uniquement au développeur de ce bot.", options=[
                create_option(
                name="action",
                description=".",
                option_type=3,
                required=False
                )])
    async def _owner(self, ctx, action: str = None):
        if ctx.author.id != 307092817942020096:
            await ctx.send(f"{ctx.author.mention} ⛔ Tu n'es pas autorisé(e) à utiliser cette commande ! ⛔")
        else:
            if action == None:
                await ctx.send("N'oublie pas d'arguments !")
            else:
                action_s = action.split(" ")
                trigger = str(action_s[0]) # actionneur : load/unload/reload
                arg = str(action_s[1]) # actionné : nom du cog

                if trigger == "load":
                    try:
                        self.bot.load_extension(f'cogs.{arg}')
                    except discord.ext.commands.errors.ExtensionAlreadyLoaded:
                        await ctx.send(f"{arg} a déjà été chargé !")
                    else:
                        await ctx.send(f"{arg} a été chargé !")
                elif trigger == "unload":
                    try:
                        self.bot.unload_extension(f'cogs.{arg}')
                    except discord.ext.commands.errors.ExtensionNotLoaded:
                        await ctx.send(f"{arg} a déjà été déchargé !")
                    else:
                        await ctx.send(f"{arg} a été déchargé !")
                elif trigger == "reload":
                    self.bot.reload_extension(f'cogs.{arg}')
                    await ctx.send(f"{arg} a été rechargé !")
                else:
                    await ctx.send("Il y a eu une erreur de déclencheur... ré-essaie :sweat_smile:")

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("owner")