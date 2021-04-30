import discord, sqlite3
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord.ext.commands import has_permissions

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="clearxp", description="Supprime les points d'expérience d'un utilisateur ! ⚠️  Nécessite la permission Administrateur.", options=[
                create_option(
                name="membre",
                description="Membre de discord",
                option_type=6,
                required=True
                )])
    async def _clearxp(self, ctx, membre: discord.Member = None):
        if ctx.author.guild_permissions.administrator:
            connection = sqlite3.connect("levels.db")
            cursor = connection.cursor()
            member_id = (f"{membre.id}",)
            guild_name = "_" + str(ctx.guild.id)
            cursor.execute('SELECT * FROM {} WHERE user_id = ?'.format(guild_name), member_id)
            member_values = cursor.fetchone()
            if member_values == None:
                await ctx.send(f"{ctx.author.mention} Tu ne peux pas réinitialiser les points d'expérience de cette personne car elle ne s'est pas inscrite à l'aventure ISO land !")
            else:
                new_level = 1
                new_exp = 0
                new_exp_goal = 500
                updated_level = (f"{new_level}", f"{membre.id}",)
                cursor.execute('UPDATE {} SET level = ? WHERE user_id = ?'.format(guild_name), updated_level)
                updated_exp = (f"{new_exp}", f"{membre.id}",)
                cursor.execute('UPDATE {} SET exp = ? WHERE user_id = ?'.format(guild_name), updated_exp)
                updated_exp_goal = (f"{new_exp_goal}", f"{membre.id}",)
                cursor.execute('UPDATE {} SET exp_goal = ? WHERE user_id = ?'.format(guild_name), updated_exp_goal)
                connection.commit()
                connection.close()
                await ctx.send(f"{ctx.author.mention} Les points d'expérience de **{membre.name}** ont bien été réinitialisés !")
        else:
            await ctx.send(f"{ctx.author.mention} Tu n'es pas autorisé à faire cette commande :angry:", delete_after=10)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("clearxp")