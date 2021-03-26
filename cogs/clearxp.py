import discord, sqlite3
from discord.ext import commands
from discord.ext.commands import has_permissions

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def clearxp(self, ctx, member: discord.Member = None):
        if ctx.message.author.guild_permissions.administrator:
            if member == None:
                await ctx.send(f"{ctx.author.mention} N'oublie pas de mentionner la personne à qui tu veux supprimer les points d'expérience ! (Si c'est toi-même, mentionne-toi.)")
            else:
                connection = sqlite3.connect("levels.db")
                cursor = connection.cursor()
                member_id = (f"{member.id}",)
                guild_name = "_" + str(ctx.guild.id)
                cursor.execute('SELECT * FROM {} WHERE user_id = ?'.format(guild_name), member_id)
                member_values = cursor.fetchone()
                if member_values == None:
                    await ctx.send(f"{ctx.author.mention} Tu ne peux pas réinitialiser les points d'expérience de cette personne car elle ne s'est pas inscrite à l'aventure ISO land !")
                else:
                    new_level = 1
                    new_exp = 0
                    new_exp_goal = 500
                    updated_level = (f"{new_level}", f"{ctx.author.id}",)
                    cursor.execute('UPDATE {} SET level = ? WHERE user_id = ?'.format(guild_name), updated_level)
                    updated_exp = (f"{new_exp}", f"{ctx.author.id}",)
                    cursor.execute('UPDATE {} SET exp = ? WHERE user_id = ?'.format(guild_name), updated_exp)
                    updated_exp_goal = (f"{new_exp_goal}", f"{ctx.author.id}",)
                    cursor.execute('UPDATE {} SET exp_goal = ? WHERE user_id = ?'.format(guild_name), updated_exp_goal)
                    connection.commit()
                    connection.close()
                    await ctx.send(f"{ctx.author.mention} Les points d'expérience de **{member.name}** ont bien été réinitialisés !")
        else:
            await ctx.send(f"{ctx.author.mention} Tu n'es pas autorisé à faire cette commande :angry:", delete_after=10)
            await ctx.message.delete()

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("clearxp")