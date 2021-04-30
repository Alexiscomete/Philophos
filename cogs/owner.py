import discord, sqlite3
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(guild_ids=[736689848626446396], name="owner", description="⛔ Commande autorisée uniquement au développeur de ce bot. bip", options=[
                create_option(
                name="action",
                description=".",
                option_type=3,
                required=True
                ),
                create_option(
                name="argument",
                description=".",
                option_type=3,
                required=False
                )])
    async def _owner(self, ctx, action: str, argument: str = None):
        if ctx.author.id != 307092817942020096:
            await ctx.send(f"{ctx.author.mention} ⛔ Tu n'es pas autorisé(e) à utiliser cette commande ! ⛔")
        else:
            if action == "load":
                try:
                    self.bot.load_extension(f'cogs.{argument}')
                except discord.ext.commands.errors.ExtensionAlreadyLoaded:
                    await ctx.send(f"{argument} a déjà été chargé !")
                else:
                    await ctx.send(f"{argument} a été chargé !")
            elif action == "unload":
                try:
                    self.bot.unload_extension(f'cogs.{argument}')
                except discord.ext.commands.errors.ExtensionNotLoaded:
                    await ctx.send(f"{argument} a déjà été déchargé !")
                else:
                    await ctx.send(f"{argument} a été déchargé !")
            elif action == "reload":
                self.bot.reload_extension(f'cogs.{argument}')
                await ctx.send(f"{argument} a été rechargé !")
            elif action == "resetcooldown":
                connection = sqlite3.connect("levels.db")
                cursor = connection.cursor()
                cursor.execute('SELECT server_id FROM levels')
                server_values = cursor.fetchall()
                print(server_values)




                await ctx.send(":ok_hand: Tous les cooldowns ont été réinitialisés !")
            else:
                await ctx.send("Il y a eu une erreur de déclencheur... ré-essaie :sweat_smile:")

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("owner")