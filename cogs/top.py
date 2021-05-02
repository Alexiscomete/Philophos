import discord, sqlite3
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="top", description="Voir le classement des systèmes d'économie !", options=[
                create_option(
                name="catégorie",
                description="Catégorie de classement",
                option_type=3,
                required=True,
                choices=[
                create_choice(
                name="rep",
                value="rep"
                ),
                create_choice(
                name="daily",
                value="daily"
                ),
                create_choice(
                name="exp",
                value="exp"
                )])])
    async def _top(self, ctx, catégorie: str):
        m_list, bs_n, counter_rep, limite_max = [], "\n", 1, 10
        if catégorie == "rep":
            connection = sqlite3.connect("iso_card.db")
            cursor = connection.cursor()
            member_id = (f"{ctx.author.id}",)
            cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
            author_values = cursor.fetchone()
            cursor.execute('SELECT * FROM tt_iso_card ORDER BY rep_points DESC')
            values = cursor.fetchall()[0:limite_max]
            if author_values != None:
                for element in values:
                    if int(element[1]) > 0:
                        member = await self.bot.fetch_user(str(element[0]))
                        if member == ctx.author:
                            author_rank = counter_rep
                            author_rep = element[1]
                            if author_rank == 1:
                                embed = discord.Embed(title="Classement des points de réputation", description="** **", color=0xFFAC33)
                            elif author_rank == 2:
                                embed = discord.Embed(title="Classement des points de réputation", description="** **", color=0xCCD6DD)
                            elif author_rank == 3:
                                embed = discord.Embed(title="Classement des points de réputation", description="** **", color=0xFF8A3B)
                            else:
                                embed = discord.Embed(title="Classement des points de réputation", description="** **")
                            m_list.append(f"#{counter_rep} **{member.name}** : {element[1]}")
                        else:
                            embed = discord.Embed(title="Classement des points de réputation", description="** **")
                            m_list.append(f"#{counter_rep} {member.name} : {element[1]}")
                        counter_rep += 1
                embed.add_field(name=f"Ta position dans le classement est : **#{author_rank}** !\nAvec un total de **{author_rep}** point(s) de réputation !", value=f"\n{bs_n.join(m_list)}", inline=False)
            else:
                embed = discord.Embed(title="Classement des points de réputation", description="** **")
                for element in values:
                    if int(element[1]) > 0:
                        member = await self.bot.fetch_user(str(element[0]))
                        m_list.append(f"#{counter_rep} {member.name} : {element[1]}")
                        counter_rep += 1
                embed.add_field(name=f"Tu n'es pas noté dans le classement car n'es pas inscrit à l'aventure ISO land...\nTu peux t'inscrire avec la commande **/start** !", value=f"\n{bs_n.join(m_list)}", inline=False)
            await ctx.send(embed=embed)

        elif catégorie == "daily":
            connection = sqlite3.connect("iso_card.db")
            cursor = connection.cursor()
            member_id = (f"{ctx.author.id}",)
            cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
            author_values = cursor.fetchone()
            cursor.execute('SELECT * FROM tt_iso_card ORDER BY dailies DESC')
            values = cursor.fetchall()[0:limite_max]
            if author_values != None:
                for element in values:
                    if int(element[5]) > 0:
                        member = await self.bot.fetch_user(str(element[0]))
                        if member == ctx.author:
                            author_rank = counter_rep
                            author_rep = element[5]
                            if author_rank == 1:
                                embed = discord.Embed(title="Classement des crédits", description="** **", color=0xFFAC33)
                            elif author_rank == 2:
                                embed = discord.Embed(title="Classement des crédits", description="** **", color=0xCCD6DD)
                            elif author_rank == 3:
                                embed = discord.Embed(title="Classement des crédits", description="** **", color=0xFF8A3B)
                            else:
                                embed = discord.Embed(title="Classement des crédits", description="** **")
                            m_list.append(f"#{counter_rep} **{member.name}** : {element[5]}")
                        else:
                            embed = discord.Embed(title="Classement des points de réputation", description="** **")
                            m_list.append(f"#{counter_rep} {member.name} : {element[5]}")
                        counter_rep += 1
                embed.add_field(name=f"Ta position dans le classement est : **#{author_rank}** !\nAvec un total de **{author_rep}** crédit(s) !", value=f"\n{bs_n.join(m_list)}", inline=False)
            else:
                embed = discord.Embed(title="Classement des crédits", description="** **")
                for element in values:
                    if int(element[5]) > 0:
                        member = await self.bot.fetch_user(str(element[0]))
                        m_list.append(f"#{counter_rep} {member.name} : {element[1]}")
                        counter_rep += 1
                embed.add_field(name=f"Tu n'es pas noté dans le classement car n'es pas inscrit à l'aventure ISO land...\nTu peux t'inscrire avec la commande **/start** !", value=f"\n{bs_n.join(m_list)}", inline=False)
            await ctx.send(embed=embed)

        elif catégorie == "exp":
            connection = sqlite3.connect("levels.db")
            cursor = connection.cursor()
            member_id = (f"{ctx.author.id}",)
            guild_name = "_" + str(ctx.guild.id)
            cursor.execute('SELECT * FROM {} WHERE user_id = ?'.format(guild_name), member_id)
            author_values = cursor.fetchone()
            cursor.execute('SELECT * FROM {} ORDER BY exp DESC'.format(guild_name)) # points d'expérience triés
            values = cursor.fetchall()[0:limite_max]
            if author_values != None:
                embed = discord.Embed(title="Classement des points d'expérience", description="** **")
                author_rank = "non classé(e)"
                author_rep = int(author_values[1])
                author_level_s = int(author_values[2])
                for element in values:
                    if int(element[1]) > 0:
                        member = await self.bot.fetch_user(str(element[0]))
                        member_id = (f"{member.id}",)
                        cursor.execute('SELECT * FROM {} WHERE user_id = ?'.format(guild_name), member_id) # niveaux triés
                        author_level = cursor.fetchone()
                        author_level_a = int(author_level[2])
                        if member == ctx.author:
                            author_level_s = author_level_a
                            author_rank = counter_rep
                            author_rep = element[1]
                            if author_rank == 1:
                                embed = discord.Embed(title="Classement des points d'expérience", description="** **", color=0xFFAC33)
                            elif author_rank == 2:
                                embed = discord.Embed(title="Classement des points d'expérience", description="** **", color=0xCCD6DD)
                            elif author_rank == 3:
                                embed = discord.Embed(title="Classement des points d'expérience", description="** **", color=0xFF8A3B)
                            else:
                                embed = discord.Embed(title="Classement des points d'expérience", description="** **")
                            m_list.append(f"#{counter_rep} **{member.name}** : {element[1]} ({author_level_a})")
                        else:
                            m_list.append(f"#{counter_rep} {member.name} : {element[1]} ({author_level_a})")
                        counter_rep += 1
                embed.add_field(name=f"Ta position dans le classement de ce serveur est : **#{author_rank}** !\nAvoir atteint le niveau **{author_level_s}** et un total de **{author_rep}** points d'expérience !", value=f"{bs_n.join(m_list)}", inline=False)
            else:
                embed = discord.Embed(title="Classement des points d'expérience", description="** **")
                for element in values:
                    if int(element[1]) > 0:
                        member = await self.bot.fetch_user(str(element[0]))
                        m_list.append(f"#{counter_rep} {member.name} : {element[1]} ({author_level_a})")
                        counter_rep += 1
                embed.add_field(name=f"Tu n'es pas noté dans le classement car n'es pas inscrit à l'aventure ISO land...\nTu peux t'inscrire avec la commande **/start** !", value=f"\n{bs_n.join(m_list)}", inline=False)
            await ctx.send(embed=embed)

        connection.close()

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("top")