import discord, sqlite3
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def top(self, ctx, top = None):
        m_list, bs_n, counter_rep, limite_max = [], "\n", 1, 10
        if top == "rep":
            async with ctx.typing():
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
                            member = await self.client.fetch_user(str(element[0]))
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
                    embed.add_field(name=f"Ta position dans le classement est : **#{author_rank}** !\nAvec un total de **{element[1]}** point(s) de réputation !", value=f"\n{bs_n.join(m_list)}", inline=False)
                else:
                    embed = discord.Embed(title="Classement des points de réputation", description="** **")
                    for element in values:
                        if int(element[1]) > 0:
                            member = await self.client.fetch_user(str(element[0]))
                            m_list.append(f"#{counter_rep} {member.name} : {element[1]}")
                            counter_rep += 1
                    embed.add_field(name=f"Tu n'es pas noté dans le classement car n'es pas inscrit à l'aventure ISO land...\nTu peux t'inscrire avec la commande **{self.client.command_prefix}start** !", value=f"\n{bs_n.join(m_list)}", inline=False)
            await ctx.send(embed=embed)

        elif top == "daily":
            async with ctx.typing():
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
                            member = await self.client.fetch_user(str(element[0]))
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
                            member = await self.client.fetch_user(str(element[0]))
                            m_list.append(f"#{counter_rep} {member.name} : {element[1]}")
                            counter_rep += 1
                    embed.add_field(name=f"Tu n'es pas noté dans le classement car n'es pas inscrit à l'aventure ISO land...\nTu peux t'inscrire avec la commande **{self.client.command_prefix}start** !", value=f"\n{bs_n.join(m_list)}", inline=False)
            await ctx.send(embed=embed)

        elif top == "exp":
            async with ctx.typing():
                connection = sqlite3.connect("levels.db")
                cursor = connection.cursor()
                member_id = (f"{ctx.author.id}",)
                guild_name = "_" + str(ctx.guild.id)
                cursor.execute('SELECT * FROM {} WHERE user_id = ?'.format(guild_name), member_id)
                author_values = cursor.fetchone()
                cursor.execute('SELECT * FROM {} ORDER BY exp DESC'.format(guild_name))
                values = cursor.fetchall()[0:limite_max]
                if author_values != None:
                    embed = discord.Embed(title="Classement des points d'expérience", description="** **")
                    author_rank = "non classée"
                    author_rep = int(author_values[1])
                    for element in values:
                        if int(element[1]) > 0:
                            member = await self.client.fetch_user(str(element[0]))
                            if member == ctx.author:
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
                                m_list.append(f"#{counter_rep} **{member.name}** : {element[1]}")
                            else:
                                m_list.append(f"#{counter_rep} {member.name} : {element[1]}")
                            counter_rep += 1
                    embed.add_field(name=f"Ta position dans le classement de ce serveur est : **#{author_rank}** !\nAvec un total de **{author_rep}** points d'expérience !", value=f"\n{bs_n.join(m_list)}", inline=False)
                else:
                    embed = discord.Embed(title="Classement des points d'expérience", description="** **")
                    for element in values:
                        if int(element[1]) > 0:
                            member = await self.client.fetch_user(str(element[0]))
                            m_list.append(f"#{counter_rep} {member.name} : {element[1]}")
                            counter_rep += 1
                    embed.add_field(name=f"Tu n'es pas noté dans le classement car n'es pas inscrit à l'aventure ISO land...\nTu peux t'inscrire avec la commande **{self.client.command_prefix}start** !", value=f"\n{bs_n.join(m_list)}", inline=False)
            await ctx.send(embed=embed)

        elif top == "level":
            async with ctx.typing():
                connection = sqlite3.connect("levels.db")
                cursor = connection.cursor()
                member_id = (f"{ctx.author.id}",)
                guild_name = "_" + str(ctx.guild.id)
                cursor.execute('SELECT * FROM {} WHERE user_id = ?'.format(guild_name), member_id)
                author_values = cursor.fetchone()
                cursor.execute('SELECT * FROM {} ORDER BY level DESC'.format(guild_name))
                values = cursor.fetchall()[0:limite_max]
                if author_values != None:
                    for element in values:
                        if int(element[2]) > 0:
                            member = await self.client.fetch_user(str(element[0]))
                            if member == ctx.author:
                                author_rank = counter_rep
                                author_rep = element[2]
                                if author_rank == 1:
                                    embed = discord.Embed(title="Classement des niveaux", description="** **", color=0xFFAC33)
                                elif author_rank == 2:
                                    embed = discord.Embed(title="Classement des niveaux", description="** **", color=0xCCD6DD)
                                elif author_rank == 3:
                                    embed = discord.Embed(title="Classement des niveaux", description="** **", color=0xFF8A3B)
                                else:
                                    embed = discord.Embed(title="Classement des niveaux", description="** **")
                                m_list.append(f"#{counter_rep} **{member.name}** : {element[2]}")
                            else:
                                m_list.append(f"#{counter_rep} {member.name} : {element[2]}")
                            counter_rep += 1
                    embed.add_field(name=f"Ta position dans le classement de ce serveur est : **#{author_rank}** !\nAvec le niveau **{author_rep}** !", value=f"\n{bs_n.join(m_list)}", inline=False)
                else:
                    embed = discord.Embed(title="Classement des niveaux", description="** **")
                    for element in values:
                        if int(element[2]) > 0:
                            member = await self.client.fetch_user(str(element[0]))
                            m_list.append(f"#{counter_rep} {member.name} : {element[1]}")
                            counter_rep += 1
                    embed.add_field(name=f"Tu n'es pas noté dans le classement car n'es pas inscrit à l'aventure ISO land...\nTu peux t'inscrire avec la commande **{self.client.command_prefix}start** !", value=f"\n{bs_n.join(m_list)}", inline=False)
            await ctx.send(embed=embed)

        else:
            await ctx.send(f"{ctx.author.mention} Ce classement n'existe pas... Tu peux afficher tous les classements existants avec **{self.client.command_prefix}help top** !")

        connection.close()

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("top")