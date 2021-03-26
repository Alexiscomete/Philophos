import discord, asyncio, sqlite3
from discord.ext import commands
from discord.ext.commands import has_permissions

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def settings(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        if ctx.message.author.guild_permissions.administrator or ctx.author.id == 307092817942020096:
            embed = discord.Embed(title=f"Bienvenue dans le menu d'édition de ton serveur !", description=ctx.author.mention)
            embed.add_field(name=":one: Afficher les informations des paramètres du bot sur ce serveur.", value="** **", inline=False)
            embed.add_field(name=":two: Créer/Modifier ton starboard.", value="** **", inline=False)
            embed.add_field(name=":three: Expérience & Niveaux", value="** **", inline=False)
            embed.add_field(name=":four: Bienvenue/Au revoir", value="** **", inline=False)
            embed.add_field(name=":x: Sortir du menu d'édition.", value="** **", inline=False)
            settings_edit = await ctx.send(embed=embed, content="> Tu as 15 secondes pour répondre.")

            try:
                msg = await self.client.wait_for("message", check=check, timeout=15)
            except asyncio.TimeoutError:
                await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
            await msg.delete()

            choice = msg.content
            if choice.lower() == "x":
                await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Edition des paramètres du serveur annulée !")

            elif choice == "1":
                connection = sqlite3.connect("levels.db")
                cursor = connection.cursor()
                server_id = (f"{ctx.guild.id}",)
                cursor.execute('SELECT * FROM levels WHERE server_id = ?', server_id)
                server_values = cursor.fetchone()
                up_message = str(server_values[1]).replace("$$AUTHOR_MENTION$$", f"{ctx.author.mention}").replace("$$AUTHOR_NAME$$", ctx.author.name).replace("$$N_LEVEL$$", "3").replace("$$A_LEVEL$$", "2")
                is_activated_xp = server_values[2]
                if is_activated_xp == "yes": is_activated_xp = ":white_check_mark:"
                elif is_activated_xp == "no": is_activated_xp = ":x:"
                is_activated_up_message = server_values[3]
                if is_activated_up_message == "no": up_message = ":x:"
                up_message_channel = server_values[4]
                if up_message_channel == "$$AUTO$$": up_message_channel = "Salon où le message est envoyé."

                embed = discord.Embed(title="Paramètres du serveur", description=ctx.author.mention)

                connection = sqlite3.connect("starboard.db")
                cursor = connection.cursor()
                server_id = (f"{ctx.guild.id}",)
                cursor.execute('SELECT * FROM starboard_generals WHERE server_id = ?', server_id)
                server_values = cursor.fetchone()

                if server_values != None:
                    is_sb_activated = server_values[1]
                    if is_sb_activated == "yes": is_sb_activated = ":white_check_mark:"
                    elif is_sb_activated == "no": is_sb_activated = ":x:"
                    embed.add_field(name="Starboard activé ?", value=is_sb_activated, inline=False)

                connection = sqlite3.connect("iso_card.db")
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM bienvenue_au_revoir WHERE server_id = ?', server_id)
                server_values = cursor.fetchone()

                if server_values != None:
                    hello_activated = server_values[3]
                    if hello_activated == "yes": hello_activated = ":white_check_mark:"
                    elif hello_activated == "no": hello_activated = ":x:"
                    embed.add_field(name="Envoi de messages d'arrivées de membres ?", value=hello_activated, inline=False)
                    goodbye_activated = server_values[4]
                    if goodbye_activated == "yes": goodbye_activated = ":white_check_mark:"
                    elif goodbye_activated == "no": goodbye_activated = ":x:"
                    embed.add_field(name="Envoi de messages de départs de membres ?", value=goodbye_activated, inline=False)
                    hello_goodbye_channel = server_values[5]
                    embed.add_field(name="Salon d'envoi des messages de départs et d'arrivées de membres", value=hello_goodbye_channel, inline=False)
                    hello_message = server_values[1].replace("$$AUTHOR_MENTION$$", f"{ctx.author.mention}").replace("$$AUTHOR_NAME$$", f"{ctx.author.name}")
                    goodbye_message = server_values[2].replace("$$AUTHOR_NAME$$", f"{ctx.author.name}")
                    embed.add_field(name="Message d'arrivée (exemple)", value=hello_message, inline=False)
                    embed.add_field(name="Message de départ (exemple)", value=goodbye_message, inline=False)

                embed.add_field(name="Système d'XP activé ?", value=is_activated_xp, inline=False)
                embed.add_field(name="UP message (exemple)", value=up_message, inline=False)
                embed.add_field(name="Salon de l'up message", value=up_message_channel, inline=False)
                await settings_edit.edit(embed=embed, content=None)
                connection.close()

            elif choice == "2":
                connection = sqlite3.connect("starboard.db")
                cursor = connection.cursor()
                server_id = (f"{ctx.guild.id}",)
                cursor.execute('SELECT * FROM starboard_generals WHERE server_id = ?', server_id)
                server_values = cursor.fetchone()
                if server_values == None:
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Ton starboard est en train d'être créé...")
                    new_server = (ctx.guild.id, "yes", 3, "⭐", "Pas lié")
                    cursor.execute('INSERT INTO starboard_generals VALUES(?, ?, ?, ?, ?)', new_server)
                    guild_name = "_" + str(ctx.guild.id)
                    create_table_s = "CREATE TABLE {}(message_id INT, channel_id INT, number_of_stars INT, bot_message_id INT, was_message_sent TEXT)".format(guild_name)
                    cursor.execute(create_table_s)
                    connection.commit()
                    server_id = (f"{ctx.guild.id}",)
                    cursor.execute('SELECT * FROM starboard_generals WHERE server_id = ?', server_id)
                    server_values = cursor.fetchone()
                    await asyncio.sleep(3)

                embed = discord.Embed(title="Bienvenue dans le menu d'édition du starboard.", description=ctx.author.mention)
                embed.add_field(name=":one: Obtenir des informations sur le starboard de ce serveur.", value="** **", inline=False)
                embed.add_field(name=":two: Activer/Désactiver le starboard.", value="** **", inline=False)
                embed.add_field(name=":three: Choisir la limite de réactions.", value="** **", inline=False)
                embed.add_field(name=":four: Choisir l'emoji qui déclenchera.", value="** **", inline=False)
                embed.add_field(name=":five: Lier un salon.", value="** **", inline=False)
                embed.add_field(name=":x: Sortir du menu d'édition.", value="** **", inline=False)
                await settings_edit.edit(embed=embed, content="> Tu as 15 secondes pour répondre.")

                try:
                    msg = await self.client.wait_for("message", check=check, timeout=15)
                except asyncio.TimeoutError:
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                await msg.delete()

                choice = msg.content
                if choice.lower() == "x":
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Edition du starboard annulée !")

                elif choice == "1":
                    server_id = (f"{ctx.guild.id}",)
                    cursor.execute('SELECT * FROM starboard_generals WHERE server_id = ?', server_id)
                    server_values = cursor.fetchone()
                    is_activated = server_values[1]
                    reactions_limit = server_values[2]
                    emoji = server_values[3]
                    bound_channel = server_values[4]
                    if is_activated == "yes":
                        is_activated = ":white_check_mark:"
                    else:
                        is_activated = "❌"
                    if bound_channel != "Pas lié":
                        bound_channel = "<#" + str(bound_channel) + ">"
                    embed = discord.Embed(title=f"Starboard du serveur {ctx.guild.name}", description=ctx.author.mention, color=0x301934)
                    embed.add_field(name="Le starboard est activé ?", value=is_activated, inline=False)
                    embed.add_field(name="Limite de réactions", value=reactions_limit, inline=True)
                    embed.add_field(name="Emoji", value=emoji, inline=True)
                    embed.add_field(name="Salon lié", value=bound_channel, inline=False)
                    await settings_edit.edit(content=None, embed=embed)

                elif choice == "2":
                    server_id = (f"{ctx.guild.id}",)
                    cursor.execute('SELECT * FROM starboard_generals WHERE server_id = ?', server_id)
                    server_values = cursor.fetchone()
                    is_activated = server_values[1]
                    if is_activated == "yes":
                        is_activated = "no"
                        actif = "désactivé"
                    else:
                        is_activated = "yes"
                        actif = "activé"
                    updated_user = (f"{is_activated}", f"{ctx.guild.id}",)
                    cursor.execute('UPDATE starboard_generals SET is_activated = ? WHERE server_id = ?', updated_user)
                    connection.commit()
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Le starboard a bien été {actif} !")

                elif choice == "3":
                    server_id = (f"{ctx.guild.id}",)
                    cursor.execute('SELECT * FROM starboard_generals WHERE server_id = ?', server_id)
                    ancienne_limite_reactions = cursor.fetchone()[2]
                    embed = discord.Embed(title="Menu de modification de la limite de réactions.", description=ctx.author.mention)
                    embed.add_field(name="Entre ci-dessous la limite pour laquelle un message sera envoyé dans le salon du starboard.", value="Entre :x: pour quitter l'édition.", inline=False)
                    await settings_edit.edit(embed=embed, content="> Tu as 15 secondes pour répondre.")
                    try:
                        msg = await self.client.wait_for("message", check=check, timeout=15)
                    except asyncio.TimeoutError:
                        await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                    await msg.delete()
                    if msg.content.lower() == "x":
                        await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Edition du starboard annulée !")
                    else:
                        try:
                            reactions_limit = int(msg.content)
                        except ValueError:
                            await settings_edit.edit(embed=None, content=f"{ctx.author.mention} La limite de réactions entrée n'est pas valide... ré-essaye !")
                        if reactions_limit < 2:
                            await settings_edit.edit(embed=None, content=f"{ctx.author.mention} La limite de réactions entrée est trop basse, son minimum est de 2 réactions !")
                        elif reactions_limit >= 2:
                            updated_user = (f"{reactions_limit}", f"{ctx.guild.id}",)
                            cursor.execute('UPDATE starboard_generals SET reactions_limit = ? WHERE server_id = ?', updated_user)
                            connection.commit()
                            await settings_edit.edit(embed=None, content=f"{ctx.author.mention} La limite a bien été redéfinie ! ({ancienne_limite_reactions} -> {reactions_limit})")

                elif choice == "4":
                    server_id = (f"{ctx.guild.id}",)
                    cursor.execute('SELECT * FROM starboard_generals WHERE server_id = ?', server_id)
                    ancien_emoji = cursor.fetchone()[3]
                    embed = discord.Embed(title="Menu de modification de l'emoji du starboard.", description=ctx.author.mention)
                    embed.add_field(name="Entre ci-dessous le salon l'emoji qui fera office de déclencheur pour le starboard.", value="Entre :x: pour quitter l'édition.", inline=False)
                    embed.add_field(name="LES EMOJIS PERSONNALISÉS DE SERVEURS DISCORD NE SONT PAS ENCORE IMPLÉMENTÉS !!!", value="** **", inline=False)
                    await settings_edit.edit(embed=embed, content="> Tu as 15 secondes pour répondre.")
                    try:
                        msg = await self.client.wait_for("message", check=check, timeout=15)
                    except asyncio.TimeoutError:
                        await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                    await msg.delete()
                    if msg.content.lower() == "x":
                        await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Edition du starboard annulée !")
                    else:
                        new_emoji = msg.content
                        updated_user = (f"{new_emoji}", f"{ctx.guild.id}",)
                        cursor.execute('UPDATE starboard_generals SET emoji_trigger = ? WHERE server_id = ?', updated_user)
                        connection.commit()
                        await settings_edit.edit(embed=None, content=f"{ctx.author.mention} L'émoji du starboard a bien été redéfini ! ({ancien_emoji} -> {new_emoji})")

                elif choice == "5":
                    server_id = (f"{ctx.guild.id}",)
                    cursor.execute('SELECT * FROM starboard_generals WHERE server_id = ?', server_id)
                    ancien_salon = cursor.fetchone()[4]
                    if ancien_salon != "Pas lié":
                        ancien_salon = "<#" + str(ancien_salon) + ">"
                    embed = discord.Embed(title="Menu de modification du salon starboard.", description=ctx.author.mention)
                    embed.add_field(name="Entre ci-dessous le salon où les messages du starboard seront envoyés.", value="Entre x pour quitter l'édition.", inline=False)
                    await settings_edit.edit(embed=embed, content="> Tu as 15 secondes pour répondre.")
                    try:
                        msg = await self.client.wait_for("message", check=check, timeout=15)
                    except asyncio.TimeoutError:
                        await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                    await msg.delete()
                    if msg.content.lower() == "x":
                        await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Edition du starboard annulée !")
                    else:
                        try:
                            bound_channel = int(msg.content.replace("<#", "").replace(">", ""))
                        except ValueError:
                            await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Le salon entré n'est pas valide... ré-essaie !")
                        updated_user = (f"{bound_channel}", f"{ctx.guild.id}",)
                        cursor.execute('UPDATE starboard_generals SET bound_channel = ? WHERE server_id = ?', updated_user)
                        connection.commit()
                        await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Le salon du starboard a bien été redéfini ! (<#{ancien_salon}> -> {msg.content})")

                else:
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Le choix que tu as entré n'est pas valide... Ré-essaie !")

            elif choice == "3":
                connection = sqlite3.connect("levels.db")
                cursor = connection.cursor()
                embed = discord.Embed(title=f"Bienvenue dans le menu d'édition des niveaux !", description=ctx.author.mention)
                embed.add_field(name=":one: Activer/Désactiver le système d'XP", value="** **", inline=False)
                embed.add_field(name=":two: Activer/Désactiver l'up message.", value="** **", inline=False)
                embed.add_field(name=":three: Editer l'up message.", value="** **", inline=False)
                embed.add_field(name=":four: Editer le salon où l'up message sera envoyé.", value="** **", inline=False)
                embed.add_field(name=":x: Sortir du menu d'édition.", value="** **", inline=False)
                embed.set_footer(text="up message = message de passage au niveau supérieur.")
                await settings_edit.edit(embed=embed, content="> Tu as 15 secondes pour répondre.")

                try:
                    msg = await self.client.wait_for("message", check=check, timeout=15)
                except asyncio.TimeoutError:
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                await msg.delete()

                choice = msg.content
                if choice.lower() == "x":
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Edition annulée !")

                elif choice == "1":
                    server_id = (f"{ctx.guild.id}",)
                    cursor.execute('SELECT * FROM levels WHERE server_id = ?', server_id)
                    server_values = cursor.fetchone()
                    is_activated = server_values[2]
                    if is_activated == "yes":
                        is_activated = "no"
                        actif = "désactivé"
                    else:
                        is_activated = "yes"
                        actif = "activé"
                    updated_server = (f"{is_activated}", f"{ctx.guild.id}",)
                    cursor.execute('UPDATE levels SET is_activated = ? WHERE server_id = ?', updated_server)
                    connection.commit()
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Le système d'XP a bien été {actif} !")

                elif choice == "2":
                    server_id = (f"{ctx.guild.id}",)
                    cursor.execute('SELECT * FROM levels WHERE server_id = ?', server_id)
                    server_values = cursor.fetchone()
                    is_activated_up_message = server_values[3]
                    if is_activated_up_message == "yes":
                        is_activated_up_message = "no"
                        actif = "désactivé"
                    else:
                        is_activated_up_message = "yes"
                        actif = "activé"
                    updated_server = (f"{is_activated_up_message}", f"{ctx.guild.id}",)
                    cursor.execute('UPDATE levels SET is_activated_up_message = ? WHERE server_id = ?', updated_server)
                    connection.commit()
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} l'up message a bien été {actif} !")

                elif choice == "3":
                    embed = discord.Embed(title="Menu de modification de l'up message.", description=ctx.author.mention)
                    embed.add_field(name="Entre ci-dessous l'up message qui sera envoyé.", value="Entre :x: pour quitter l'édition.", inline=False)
                    embed.add_field(name="** **", value="```$$AUTHOR_MENTION$$ = mention du membre\n$$AUTHOR_NAME$$ = nom du membre\n$$A_LEVEL$$ = ancien niveau\n$$N_LEVEL$$ = nouveau niveau```", inline=False)
                    await settings_edit.edit(embed=embed, content="> Tu as 1 minute pour répondre.")

                    try:
                        msg = await self.client.wait_for("message", check=check, timeout=60)
                    except asyncio.TimeoutError:
                        await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                    await msg.delete()

                    new_up_message = msg.content

                    updated_server = (f"{new_up_message}", f"{ctx.guild.id}",)
                    cursor.execute('UPDATE levels SET up_message = ? WHERE server_id = ?', updated_server)
                    connection.commit()

                    embed = discord.Embed(description=new_up_message)
                    await settings_edit.edit(embed=embed, content="> L'up message a été mise à jour !")

                elif choice == "4":
                    embed = discord.Embed(title="Menu de modification du salon de l'up message", description=ctx.author.mention)
                    embed.add_field(name="Entre ci-dessous le salon où l'up message sera envoyé.", value="Entre :x: pour quitter l'édition.", inline=False)
                    embed.add_field(name="** **", value="```$$AUTO$$ = salon où le membre parle.```", inline=False)
                    await settings_edit.edit(embed=embed, content="> Tu as 1 minute pour répondre.")

                    try:
                        msg = await self.client.wait_for("message", check=check, timeout=60)
                    except asyncio.TimeoutError:
                        await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                    await msg.delete()

                    new_channel_up_message = msg.content

                    updated_server = (f"{new_channel_up_message}", f"{ctx.guild.id}",)
                    cursor.execute('UPDATE levels SET channel_to_send = ? WHERE server_id = ?', updated_server)
                    connection.commit()

                    embed = discord.Embed(description=new_channel_up_message)
                    await settings_edit.edit(embed=embed, content="> Le salon de l'up message a été mis à jour !")

            elif choice == "4":
                connection = sqlite3.connect("iso_card.db")
                cursor = connection.cursor()

                server_id = (f"{ctx.guild.id}",)
                cursor.execute('SELECT * FROM bienvenue_au_revoir WHERE server_id = ?', server_id)
                server_values = cursor.fetchone()

                if server_values == None:
                    new_server = (ctx.guild.id, "Un nouveau membre a rejoint le serveur !", "Un membre a quitté le serveur...", "no", "no", "Pas lié")
                    cursor.execute('INSERT INTO bienvenue_au_revoir VALUES(?, ?, ?, ?, ?, ?)', new_server)
                    connection.commit()
                    server_id = (f"{ctx.guild.id}",)
                    cursor.execute('SELECT * FROM bienvenue_au_revoir WHERE server_id = ?', server_id)
                    server_values = cursor.fetchone()

                embed = discord.Embed(title=f"Bienvenue dans le menu d'édition des messages d'arrivée/départ des membres !", description=ctx.author.mention)
                embed.add_field(name=":one: Activer/désactiver le message d'arrivée des membres.", value="** **", inline=False)
                embed.add_field(name=":two: Activer/désactiver le message de départ des membres.", value="** **", inline=False)
                embed.add_field(name=":three: Editer le message d'arrivée des membres.", value="** **", inline=False)
                embed.add_field(name=":four: Editer le message de départ des membres.", value="** **", inline=False)
                embed.add_field(name=":five: Editer le salon d'envoi des messages.", value="** **", inline=False)
                embed.add_field(name=":x: Sortir du menu d'édition.", value="** **", inline=False)
                await settings_edit.edit(embed=embed, content="> Tu as 15 secondes pour répondre.")

                try:
                    msg = await self.client.wait_for("message", check=check, timeout=15)
                except asyncio.TimeoutError:
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                await msg.delete()

                choice = msg.content
                if choice.lower() == "x":
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Edition annulée !")
                elif choice == "1":
                    is_activated_hello = server_values[3]
                    if is_activated_hello == "yes":
                        is_activated_hello = "no"
                        actif = "désactivé"
                    else:
                        is_activated_hello = "yes"
                        actif = "activé"
                    updated_server = (f"{is_activated_hello}", f"{ctx.guild.id}",)
                    cursor.execute('UPDATE bienvenue_au_revoir SET hello_activated = ? WHERE server_id = ?', updated_server)
                    connection.commit()
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} L'envoi des messages d'arrivée de membres a bien été {actif} !")

                elif choice == "2":
                    is_activated_goodbye = server_values[4]
                    if is_activated_goodbye == "yes":
                        is_activated_goodbye = "no"
                        actif = "désactivé"
                    else:
                        is_activated_goodbye = "yes"
                        actif = "activé"
                    updated_server = (f"{is_activated_goodbye}", f"{ctx.guild.id}",)
                    cursor.execute('UPDATE bienvenue_au_revoir SET goodbye_activated = ? WHERE server_id = ?', updated_server)
                    connection.commit()
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} L'envoi des messages de départ de membres a bien été {actif} !")

                elif choice == "3":

                    embed = discord.Embed(title="Menu de modification du message d'arrivée d'un membre", description=ctx.author.mention)
                    embed.add_field(name="Entre ci-dessous le message pour indiquer l'arrivée d'un membre.", value="Entre :x: pour quitter l'édition.", inline=False)
                    embed.add_field(name="** **", value="```$$AUTHOR_MENTION$$ = mention du membre\n$$AUTHOR_NAME$$ = nom du membre```", inline=False)
                    await settings_edit.edit(embed=embed, content="> Tu as 1 minute pour répondre.")

                    ancient_hello_message = server_values[1]

                    try:
                        msg = await self.client.wait_for("message", check=check, timeout=60)
                    except asyncio.TimeoutError:
                        await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                    await msg.delete()

                    hello_message = msg.content

                    updated_server = (f"{hello_message}", f"{ctx.guild.id}",)
                    cursor.execute('UPDATE bienvenue_au_revoir SET hello_message = ? WHERE server_id = ?', updated_server)
                    connection.commit()
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Le salon d'envoi des messages de départs et d'arrivés de membres a été actualisé !\n> {ancient_hello_message} ===> {hello_message}")

                elif choice == "4":

                    embed = discord.Embed(title="Menu de modification du message de départ d'un membre", description=ctx.author.mention)
                    embed.add_field(name="Entre ci-dessous le message pour indiquer le départ d'un membre.", value="Entre :x: pour quitter l'édition.", inline=False)
                    embed.add_field(name="** **", value="```$$AUTHOR_NAME$$ = nom du membre```", inline=False)
                    await settings_edit.edit(embed=embed, content="> Tu as 1 minute pour répondre.")

                    ancient_goodbye_message = server_values[2]

                    try:
                        msg = await self.client.wait_for("message", check=check, timeout=60)
                    except asyncio.TimeoutError:
                        await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                    await msg.delete()

                    goodbye_message = msg.content

                    updated_server = (f"{goodbye_message}", f"{ctx.guild.id}",)
                    cursor.execute('UPDATE bienvenue_au_revoir SET goodbye_message = ? WHERE server_id = ?', updated_server)
                    connection.commit()
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Le message pour indiquer le départ d'un membre a été actualisé !\n> {ancient_goodbye_message} ===> {goodbye_message}")

                elif choice == "5":

                    embed = discord.Embed(title="Menu de modification du salon des messages de départs et d'arrivés de membres", description=ctx.author.mention)
                    embed.add_field(name="Entre ci-dessous le salon où seront envoyés les messages pour indiquer l'arrivée ou le départ d'un membre.", value="Entre :x: pour quitter l'édition.", inline=False)
                    await settings_edit.edit(embed=embed, content="> Tu as 1 minute pour répondre.")

                    ancient_hello_goodbye_channel = server_values[5]

                    try:
                        msg = await self.client.wait_for("message", check=check, timeout=60)
                    except asyncio.TimeoutError:
                        await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                    await msg.delete()

                    hello_goodbye_channel = msg.content

                    updated_server = (f"{hello_goodbye_channel}", f"{ctx.guild.id}",)
                    cursor.execute('UPDATE bienvenue_au_revoir SET hello_goodbye_channel = ? WHERE server_id = ?', updated_server)
                    connection.commit()
                    await settings_edit.edit(embed=None, content=f"{ctx.author.mention} Le message pour indiquer l'arrivée d'un membre a été actualisé !\n> {ancient_hello_goodbye_channel} ===> {hello_goodbye_channel}")

            connection.close()
        else:
            await ctx.send(f"{ctx.author.mention} Tu n'as pas la permission de faire cela sur ce serveur :angry:")

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("settings")