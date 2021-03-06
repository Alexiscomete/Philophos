import discord, sqlite3, asyncio
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['profile'])
    async def card(self, ctx, arg = None):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        espace = " "
        if arg == None:
            member = ctx.author
        if arg != "edit" and arg != None:
            try:
                member = await self.client.fetch_user(str(arg).replace("<@",'').replace(">",'').replace("!",''))
            except discord.errors.HTTPException:
                await ctx.send(f"{ctx.author.mention} L'utilisateur recherché n'a pas été trouvé...")
        if arg == None or arg != "edit":
            if member.bot == True:
                await ctx.send(f"{ctx.author.mention} Les bots n'ont pas de carte... :wink:")
            if member.bot == False:
                member_id = (f"{member.id}",)
                cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
                if cursor.fetchone() == None:
                    if member == ctx.author:
                        await ctx.send("Tu ne peux pas afficher ta carte car tu n'as pas commencé l'aventure ISO land ! (Pour débuter, fait : **+start**)")
                    else:
                        await ctx.send("Tu ne peux pas afficher la carte de cette personne car elle ne s'est pas inscrite à l'aventure ISO land... (Elle peut débuter en faisant **+start**)")
                else:
                    cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
                    member_values = cursor.fetchone()
                    guild_name = "_" + str(ctx.guild.id)
                    rep_points = member_values[1] #member_values[0] = user_id
                    archi_list = member_values[2]
                    about_para = member_values[3]
                    afk_status = member_values[4]
                    daily = member_values[5]

                    if about_para == "":
                        about_para = "Je suis un nouveau dans l'aventure d'ISO land !"
                    embed = discord.Embed(title=f"aCard de {member.name}", description=member.mention, color=0xf9c62d)
                    embed.add_field(name="À propos", value=about_para, inline=False)
                    if afk_status != "None":
                        embed.add_field(name="Statut AFK", value=afk_status, inline=False)
                    embed.add_field(name="<:reputation_point:810240527941238835> Point(s) de réputation", value=rep_points, inline=True)
                    embed.add_field(name="<:aCoin:813464075249123339> Crédits", value=daily, inline=True)
                    embed.add_field(name=":trophy: Succès", value=archi_list, inline=False)
                    await ctx.send(embed=embed)

        if arg == "edit":
            member_id = (f"{ctx.author.id}",)
            cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
            if cursor.fetchone() == None:
                await ctx.send("Tu ne peux pas éditer ta carte car tu n'as pas commencé l'aventure ISO land ! (Pour débuter, fait : **+start**)")
            else:
                embed = discord.Embed(title="Bienvenue dans le menu d'édition de ta carte", description=ctx.author.mention)
                embed.add_field(name=":one: Editer la section 'à propos'", value="** **", inline=False)
                embed.add_field(name=":two: Ajouter/Editer ton statut AFK", value="** **", inline=False)
                embed.add_field(name=":x: Sortir du menu d'édition.", value="** **", inline=False)
                card_edit_m = await ctx.send(embed=embed, content="> Tu as 10 secondes pour répondre.")

                try:
                    msg = await self.client.wait_for("message", check=check, timeout=10)
                except asyncio.TimeoutError:
                    await card_edit_m.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                await msg.delete()

                choice = msg.content
                if choice.lower() == "x":
                    await card_edit_m.edit(embed=None, content=f"{ctx.author.mention} Edition de la carte annulée !")
                elif choice == "1":
                    embed = discord.Embed(title="Menu de modification de la section 'à propos'", description=ctx.author.mention)
                    embed.add_field(name="Entrez ci-dessous le texte à mettre dans la description de ta carte.", value="Entre :x: pour quitter l'édition.", inline=False)
                    await card_edit_m.edit(embed=embed, content="> Tu as 30 secondes pour répondre.")
                    try:
                        msg = await self.client.wait_for("message", check=check, timeout=30)
                    except asyncio.TimeoutError:
                        await card_edit_m.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")

                    new_about_para = msg.content

                    if new_about_para.lower() == "x":
                        await msg.delete()
                        await card_edit_m.edit(embed=None, content=f"{ctx.author.mention} Edition de la carte annulée !")
                    else:
                        if len(list(str(new_about_para))) > 100:
                            await card_edit_m.edit(embed=None, content=f"{ctx.author.mention} Ce statut ne peut pas être validé car il dépasse la limite de 100 caractères.")
                        else:
                            await msg.delete()
                            member_id = (f"{ctx.author.id}",)
                            cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
                            updated_user = (f"{new_about_para}", f"{ctx.author.id}",)
                            cursor.execute('UPDATE tt_iso_card SET about = ? WHERE user_id = ?', updated_user)
                            connection.commit()
                            embed = discord.Embed(description=new_about_para)
                            await card_edit_m.edit(embed=embed, content="Le contenu **à propos** de ta carte a bien été actualisé !")

                elif choice == "2":
                    embed = discord.Embed(title="Menu de modification de ton statut AFK", description=ctx.author.mention)
                    embed.add_field(name="Entrez ci-dessous le texte à mettre dans ton statut AFK.", value="Entre :x: pour quitter l'édition.", inline=False)
                    await card_edit_m.edit(embed=embed, content="> Tu as 30 secondes pour répondre.")
                    try:
                        msg = await self.client.wait_for("message", check=check, timeout=30)
                    except asyncio.TimeoutError:
                        await card_edit_m.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")

                    afk_statut = msg.content
                    await msg.delete()
                    updated_user = (f"{afk_statut}", f"{ctx.author.id}",)
                    cursor.execute('UPDATE tt_iso_card SET afk = ? WHERE user_id = ?', updated_user)
                    connection.commit()
                    embed = discord.Embed(description=afk_statut)
                    await card_edit_m.edit(embed=embed, content=f"{ctx.author.mention} Ton statut AFK a bien été enregistré !")

                else:
                    await card_edit_m.edit(embed=None, content=f"{ctx.author.mention} Le choix que tu as entré n'est pas valide... Ré-essaye !")

        connection.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        member_id = (f"{message.author.id}",)
        cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
        author_values_2 = cursor.fetchone()
        if author_values_2 != None:
            is_afk = author_values_2[4]
            if message and not message.content.startswith("+afk") and message.author.bot == False and is_afk != "None":
                updated_user = ("None", f"{message.author.id}",)
                cursor.execute('UPDATE tt_iso_card SET afk = ? WHERE user_id = ?', updated_user)
                connection.commit()
                await message.channel.send(f"{message.author.mention} Tu es de retour ! Ton statut AFK a donc été désactivé.", delete_after=10)

        if message and not message.content.startswith("+afk") and not message.content.startswith("+card") and message.author.bot == False:
            for user in message.mentions:
                member_id = (f"{user.id}",)
                cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
                user_afk_s = cursor.fetchone()
                user_afk_s = user_afk_s[4]
                if user_afk_s != "None":
                    await message.channel.send(f"{message.author.mention} Désolé mais l'utilisateur ({user.name}) que tu as mentionné est actuellement en AFK. Voici le statut qu'il/elle a laissé :\n> {user_afk_s}")

        connection.close()

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("card")