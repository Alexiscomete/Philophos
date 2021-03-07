import discord, sqlite3, asyncio
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def setprefix(self, ctx, prefixe = None):
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        if prefixe == None:
            await ctx.send(f"{ctx.author.mention} N'oublie pas de spécifier le nouveau préfixe !")
        prefix_l = prefixe.split(" ")
        if len(prefix_l) > 1:
            await ctx.send(f"{ctx.author.mention} Ce préfixe est invalide car il est plus grand qu'un mot !")
        if prefixe != None and len(prefix_l) == 1:
            server_id = (f"{ctx.guild.id}",)
            cursor.execute('SELECT * FROM prefixes WHERE server_id = ?', server_id)
            server_values = cursor.fetchone()
            if server_values == None:
                new_server = (ctx.guild.id, "+")
                cursor.execute('INSERT INTO prefixes VALUES(?, ?)', new_server)
                connection.commit()

            ancient_prefix = server_values[1]
            new_prefix = prefixe
            updated_server = (f"{new_prefix}", f"{ctx.guild.id}",)
            cursor.execute('UPDATE prefixes SET prefix = ? WHERE server_id = ?', updated_server)
            connection.commit()

            await ctx.send(f"{ctx.author.mention} Le préfixe de ce serveur a bien été actualisé !\n> **{ancient_prefix}** => **{new_prefix}**")

        connection.close()

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("setprefix")