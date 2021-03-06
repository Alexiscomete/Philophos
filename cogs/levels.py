import discord, sqlite3, random, asyncio, json
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):

        channel = self.client.get_channel(774688147199492137)

        if message.author.bot == False and message.guild.id != 401667451189985280: # ajouter une ligne/créer une table
            connection = sqlite3.connect("levels.db") # pour un serveur qui
            cursor = connection.cursor() # n'est pas encore enregistré dans la BDD
            server_id = (f"{message.guild.id}",)
            cursor.execute('SELECT * FROM levels WHERE server_id = ?', server_id)
            server_values = cursor.fetchone()
            if server_values == None:
                new_server = (message.guild.id, "$$AUTHOR_MENTION$$ :up: Tu as évolué d'un niveau ! (**$$A_LEVEL$$** => **$$N_LEVEL$$**)", "yes")
                cursor.execute('INSERT INTO levels VALUES(?, ?, ?)', new_server)
                guild_name = "_" + str(message.guild.id)
                create_table_s = "CREATE TABLE {}(user_id INT, exp INT, level INT, exp_goal INT, cooldown TEXT)".format(guild_name)
                cursor.execute(create_table_s)
                connection.commit()

            server_id = (f"{message.guild.id}",)
            cursor.execute('SELECT * FROM levels WHERE server_id = ?', server_id)
            server_values = cursor.fetchone()

            if server_values[2] == "yes":

                user_id = (f"{message.author.id}",) # recherche d'un membre dans la BDD
                guild_name = "_" + str(message.guild.id) # du serveur où est le membre
                cursor.execute('SELECT * FROM {} WHERE user_id = ?'.format(guild_name), user_id)
                user_values = cursor.fetchone()

                if user_values == None: # ajout d'une ligne pour le membre dans
                    guild_name = "_" + str(message.guild.id) # la BDD du serveur
                    new_user = (message.author.id, 0, 1, 500, "no")
                    cursor.execute('INSERT INTO {} VALUES(?, ?, ?, ?, ?)'.format(guild_name), new_user)
                    connection.commit()

                user_id = (f"{message.author.id}",) # actualisation des données du membre
                guild_name = "_" + str(message.guild.id) # dans la BDD du serveur
                cursor.execute('SELECT * FROM {} WHERE user_id = ?'.format(guild_name), user_id)
                user_values = cursor.fetchone()

                if user_values != None and user_values[4] == "no": # vérification du
                    updated_user = ("yes", f"{message.author.id}",) # cooldown du membre,
                    guild_name = "_" + str(message.guild.id) # indépendant sur chaque serveur
                    cursor.execute('UPDATE {} SET cooldown = ? WHERE user_id = ?'.format(guild_name), updated_user)
                    connection.commit()

                    server_id = (f"{message.guild.id}",)
                    cursor.execute('SELECT * FROM levels WHERE server_id = ?', server_id)
                    server_values = cursor.fetchone()
                    if server_values != None:
                        up_message = str(server_values[1])

                    exp = int(user_values[1])
                    new_exp = exp + random.randint(10, 40)
                    updated_user = (f"{new_exp}", f"{message.author.id}",)
                    level = int(user_values[2])
                    exp_goal = int(user_values[3])

                    if new_exp >= exp_goal:
                        guild_name = "_" + str(message.guild.id)
                        ancien_level = level
                        level += 1
                        up_message = up_message.replace("$$AUTHOR_MENTION$$", f"{str(message.author.mention)}").replace("$$A_LEVEL$$", f"{str(ancien_level)}").replace("$$N_LEVEL$$", f"{str(level)}")
                        updated_level = (f"{level}", f"{message.author.id}",)
                        cursor.execute('UPDATE {} SET level = ? WHERE user_id = ?'.format(guild_name), updated_level)
                        exp_goal = round(exp*1.05 + ancien_level*75)
                        updated_exp = (f"{exp_goal}", f"{message.author.id}",)
                        cursor.execute('UPDATE {} SET exp_goal = ? WHERE user_id = ?'.format(guild_name), updated_exp)
                        connection.commit()

                        await message.channel.send(up_message)

                    guild_name = "_" + str(message.guild.id)
                    cursor.execute('UPDATE {} SET exp = ? WHERE user_id = ?'.format(guild_name), updated_user)
                    connection.commit()
                    await asyncio.sleep(60)
                    updated_user = ("no", f"{message.author.id}",)
                    cursor.execute('UPDATE {} SET cooldown = ? WHERE user_id = ?'.format(guild_name), updated_user)
                    connection.commit()

            connection.close()

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("levels")