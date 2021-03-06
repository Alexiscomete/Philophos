import discord, asyncio, sqlite3
from discord.ext import commands
from discord.ext.commands import has_permissions

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        connection = sqlite3.connect("starboard.db")
        cursor = connection.cursor()
        server_id = (f"{payload.guild_id}",)
        cursor.execute('SELECT * FROM starboard_generals WHERE server_id = ?', server_id)
        server_values = cursor.fetchone()
        if server_values != None and server_values[1] == "yes":
            if payload.emoji.name == str(server_values[3]):
                message_id_cursor = 'SELECT * FROM {} WHERE message_id = {}'.format(f"_{payload.guild_id}", payload.message_id)
                cursor.execute(message_id_cursor)
                message_values = cursor.fetchone()

                if message_values == None:
                    new_message = (int(payload.message_id), int(payload.channel_id), 1, 0, "no")
                    cursor.execute('INSERT INTO {} VALUES(?, ?, ?, ?, ?)'.format(f"_{payload.guild_id}"), new_message)
                    connection.commit()
                else:
                    nb_stars = int(message_values[2])
                    if nb_stars >= 0:
                        new_nb_of_stars = nb_stars + 1
                        updated_user = (f"{new_nb_of_stars}", f"{payload.message_id}",)
                        cursor.execute('UPDATE {} SET number_of_stars = ? WHERE message_id = ?'.format(f"_{payload.guild_id}"), updated_user)
                        connection.commit()

                        message_id = (f"{payload.message_id}",)
                        cursor.execute('SELECT * FROM {} WHERE message_id = ?'.format(f"_{payload.guild_id}"), message_id)
                        messages_values_f = cursor.fetchone()
                        server_id = (f"{payload.guild_id}",)
                        cursor.execute('SELECT * FROM starboard_generals WHERE server_id = ?', server_id)
                        message_values = cursor.fetchone()

                        chosen_emoji = message_values[3]
                        number_of_stars = int(messages_values_f[2])
                        was_message_sent = messages_values_f[4]
                        limit_trigger = message_values[2]

                        if number_of_stars == limit_trigger:
                            if was_message_sent == "no":
                                was_message_sent = "yes"
                                channel_to_send = self.client.get_channel(int(message_values[4]))
                                channel_to_find = self.client.get_channel(payload.channel_id)
                                msg = await channel_to_find.fetch_message(payload.message_id)
                                embed = discord.Embed(title="Nouveau message sur le starboard !", description=f"de {msg.author.mention} | [ID du message](https://discord.com/channels/736689848626446396/{msg.channel.id}/{msg.id})")
                                try:
                                    embed.set_image(url=msg.attachments[0].url)
                                except IndexError:
                                    pass
                                embed.add_field(name=f"{number_of_stars} {chosen_emoji}", value="** **", inline=False)
                                if msg.content:
                                    embed.add_field(name="** **", value=msg.content, inline=False)
                                bot_message = await channel_to_send.send(embed=embed)
                                updated_user = (f"{bot_message.id}", f"{payload.message_id}",)
                                cursor.execute('UPDATE {} SET bot_message_id = ? WHERE message_id = ?'.format(f"_{payload.guild_id}"), updated_user)
                                updated_message_s = (f"{was_message_sent}", f"{payload.message_id}",)
                                cursor.execute('UPDATE {} SET was_message_sent = ? WHERE message_id = ?'.format(f"_{payload.guild_id}"), updated_message_s)
                                connection.commit()
                        elif number_of_stars > limit_trigger:
                            cursor.execute('SELECT * FROM {} WHERE message_id = ?'.format(f"_{payload.guild_id}"), message_id)
                            messages_values_b = cursor.fetchone()
                            b_msg = messages_values_b[3]
                            channel_to_find = self.client.get_channel(int(message_values[4]))
                            msg_bot = await channel_to_find.fetch_message(b_msg)

                            channel_to_send = self.client.get_channel(int(message_values[4]))
                            channel_to_find = self.client.get_channel(payload.channel_id)
                            msg = await channel_to_find.fetch_message(payload.message_id)

                            embed = discord.Embed(title="Nouveau message sur le starboard !", description=f"de {msg.author.mention}")
                            try:
                                embed.set_image(url=msg.attachments[0].url)
                            except IndexError:
                                pass
                            embed.add_field(name=f"{number_of_stars} :star:", value=msg.content, inline=False)
                            embed.add_field(name="** **", value=f"[ID du message](https://discord.com/channels/736689848626446396/{msg.channel.id}/{msg.id})", inline=False)
                            await msg_bot.edit(content=None, embed=embed)

        connection.close()

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        connection = sqlite3.connect("starboard.db")
        cursor = connection.cursor()
        server_id = (f"{payload.guild_id}",)
        cursor.execute('SELECT * FROM starboard_generals WHERE server_id = ?', server_id)
        server_values = cursor.fetchone()
        if server_values != None and server_values[1] == "yes":
            if payload.emoji.name == str(server_values[3]):
                message_id = (f"{payload.message_id}",)
                cursor.execute('SELECT * FROM {} WHERE message_id = ?'.format(f"_{payload.guild_id}"), message_id)
                message_values = cursor.fetchone()

                nb_stars = int(message_values[2])
                new_nb_of_stars = nb_stars - 1
                updated_user = (f"{new_nb_of_stars}", f"{payload.message_id}",)
                cursor.execute('UPDATE {} SET number_of_stars = ? WHERE message_id = ?'.format(f"_{payload.guild_id}"), updated_user)
                connection.commit()

                connection.close()

    @commands.command()
    async def starboard(self, ctx, arg = None):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        if ctx.message.author.guild_permissions.administrator:
            connection = sqlite3.connect("starboard.db")
            cursor = connection.cursor()
            if arg == "create":
                server_id = (f"{ctx.guild.id}",)
                cursor.execute('SELECT * FROM starboard_generals WHERE server_id = ?', server_id)
                server_values = cursor.fetchone()
                if server_values == None:
                    new_server = (ctx.guild.id, "yes", 3, "⭐", "Pas lié")
                    cursor.execute('INSERT INTO starboard_generals VALUES(?, ?, ?, ?, ?)', new_server)
                    guild_name = "_" + str(ctx.guild.id)
                    create_table_s = "CREATE TABLE {}(message_id INT, channel_id INT, number_of_stars INT, bot_message_id INT, was_message_sent TEXT)".format(guild_name)
                    cursor.execute(create_table_s)
                    connection.commit()
                    await ctx.send(f"{ctx.author.mention} Ton starboard a bien été créé !")
                else:
                    await ctx.send("Tu as déjà un starboard... tu ne peux pas en créer un autre sur ce serveur.")
            elif arg != "create" and arg != None:
                await ctx.send(f"{ctx.author.mention} Une erreur s'est produite... ré-essaye la commande ! :wink:")
            elif arg == None:
                server_id = (f"{ctx.guild.id}",)
                cursor.execute('SELECT * FROM starboard_generals WHERE server_id = ?', server_id)
                server_values = cursor.fetchone()
                if server_values == None:
                    await ctx.send(f"{ctx.author.mention} Désolé mais tu ne peux pas modifier ton starboard car tu n'en as pas créé. Si tu veux en créer un, fait **+starboard create** !")
                else:
                    embed = discord.Embed(title="Bienvenue dans le menu d'édition du starboard.", description=ctx.author.mention)
                    embed.add_field(name=":one: Obtenir des informations sur le starboard de ce serveur.", value="** **", inline=False)
                    embed.add_field(name=":two: Activer/Désactiver le starboard.", value="** **", inline=False)
                    embed.add_field(name=":three: Choisir la limite de réactions.", value="** **", inline=False)
                    embed.add_field(name=":four: Choisir l'emoji qui déclenchera.", value="** **", inline=False)
                    embed.add_field(name=":five: Lier un salon.", value="** **", inline=False)
                    embed.add_field(name="❌ Sortir du menu d'édition.", value="** **", inline=False)
                    starboard_edit = await ctx.send(embed=embed, content="> Tu as 15 secondes pour répondre.")

                    try:
                        msg = await self.client.wait_for("message", check=check, timeout=15)
                    except asyncio.TimeoutError:
                        await starboard_edit.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                    await msg.delete()

                    choice = msg.content
                    if choice == "❌":
                        await starboard_edit.edit(embed=None, content=f"{ctx.author.mention} Edition du starboard annulée !")

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
                        await starboard_edit.edit(content=None, embed=embed)

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
                        await starboard_edit.edit(embed=None, content=f"{ctx.author.mention} Le starboard a bien été {actif} !")

                    elif choice == "3":
                        server_id = (f"{ctx.guild.id}",)
                        cursor.execute('SELECT * FROM starboard_generals WHERE server_id = ?', server_id)
                        ancienne_limite_reactions = cursor.fetchone()[2]
                        embed = discord.Embed(title="Menu de modification de la limite de réactions.", description=ctx.author.mention)
                        embed.add_field(name="Entre ci-dessous la limite pour laquelle un message sera envoyé dans le salon du starboard.", value="Entre ❌ pour quitter l'édition.", inline=False)
                        await starboard_edit.edit(embed=embed, content="> Tu as 15 secondes pour répondre.")
                        try:
                            msg = await self.client.wait_for("message", check=check, timeout=15)
                        except asyncio.TimeoutError:
                            await starboard_edit.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                        await msg.delete()
                        if msg.content == "❌":
                            await starboard_edit.edit(embed=None, content=f"{ctx.author.mention} Edition du starboard annulée !")
                        else:
                            try:
                                reactions_limit = int(msg.content)
                            except ValueError:
                                await starboard_edit.edit(embed=None, content=f"{ctx.author.mention} La limite de réactions entrée n'est pas valide... ré-essaye !")
                            if reactions_limit < 2:
                                await starboard_edit.edit(embed=None, content=f"{ctx.author.mention} La limite de réactions entrée est trop basse, son minimum est de 2 réactions !")
                            elif reactions_limit >= 2:
                                updated_user = (f"{reactions_limit}", f"{ctx.guild.id}",)
                                cursor.execute('UPDATE starboard_generals SET reactions_limit = ? WHERE server_id = ?', updated_user)
                                connection.commit()
                                await starboard_edit.edit(embed=None, content=f"{ctx.author.mention} La limite a bien été redéfinie ! ({ancienne_limite_reactions} -> {reactions_limit})")

                    elif choice == "4":
                        server_id = (f"{ctx.guild.id}",)
                        cursor.execute('SELECT * FROM starboard_generals WHERE server_id = ?', server_id)
                        ancien_emoji = cursor.fetchone()[3]
                        embed = discord.Embed(title="Menu de modification de l'emoji du starboard.", description=ctx.author.mention)
                        embed.add_field(name="Entre ci-dessous le salon l'emoji qui fera office de déclencheur pour le starboard.", value="Entre ❌ pour quitter l'édition.", inline=False)
                        embed.add_field(name="LES EMOJIS PERSONNALISÉS DE SERVEURS DISCORD NE SONT PAS ENCORE IMPLÉMENTÉS !!!", value="** **", inline=False)
                        await starboard_edit.edit(embed=embed, content="> Tu as 15 secondes pour répondre.")
                        try:
                            msg = await self.client.wait_for("message", check=check, timeout=15)
                        except asyncio.TimeoutError:
                            await starboard_edit.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                        await msg.delete()
                        if msg.content == "❌":
                            await starboard_edit.edit(embed=None, content=f"{ctx.author.mention} Edition du starboard annulée !")
                        else:
                            new_emoji = msg.content
                            updated_user = (f"{new_emoji}", f"{ctx.guild.id}",)
                            cursor.execute('UPDATE starboard_generals SET emoji_trigger = ? WHERE server_id = ?', updated_user)
                            connection.commit()
                            await starboard_edit.edit(embed=None, content=f"{ctx.author.mention} L'émoji du starboard a bien été redéfini ! ({ancien_emoji} -> {new_emoji})")

                    elif choice == "5":
                        server_id = (f"{ctx.guild.id}",)
                        cursor.execute('SELECT * FROM starboard_generals WHERE server_id = ?', server_id)
                        ancien_salon = cursor.fetchone()[4]
                        if ancien_salon != "Pas lié":
                            ancien_salon = "<#" + str(ancien_salon) + ">"
                        embed = discord.Embed(title="Menu de modification du salon starboard.", description=ctx.author.mention)
                        embed.add_field(name="Entre ci-dessous le salon où les messages du starboard seront envoyés.", value="Entre ❌ pour quitter l'édition.", inline=False)
                        await starboard_edit.edit(embed=embed, content="> Tu as 15 secondes pour répondre.")
                        try:
                            msg = await self.client.wait_for("message", check=check, timeout=15)
                        except asyncio.TimeoutError:
                            await starboard_edit.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                        await msg.delete()
                        if msg.content == "❌":
                            await starboard_edit.edit(embed=None, content=f"{ctx.author.mention} Edition du starboard annulée !")
                        else:
                            try:
                                bound_channel = int(msg.content.replace("<#", "").replace(">", ""))
                            except ValueError:
                                await starboard_edit.edit(embed=None, content=f"{ctx.author.mention} Le salon entré n'est pas valide... ré-essaie !")
                            updated_user = (f"{bound_channel}", f"{ctx.guild.id}",)
                            cursor.execute('UPDATE starboard_generals SET bound_channel = ? WHERE server_id = ?', updated_user)
                            connection.commit()
                            await starboard_edit.edit(embed=None, content=f"{ctx.author.mention} Le salon du starboard a bien été redéfini ! (<#{ancien_salon}> -> {msg.content})")

                    else:
                        await starboard_edit.edit(embed=None, content=f"{ctx.author.mention} Le choix que tu as entré n'est pas valide... Ré-essaie !")

            connection.close()

        else:
            await ctx.send(f"{ctx.author.mention} Tu n'as pas la permission de créer ou d'éditer un starboard sur ce serveur :angry:")

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("starboard")