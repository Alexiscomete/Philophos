import discord, sqlite3
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def start(self, ctx):
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        member_id = (f"{ctx.author.id}",)
        cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
        if cursor.fetchone() == None:
            new_user = (ctx.author.id, 0, ":beginner:", "Je suis un nouveau dans l'aventure d'ISO land !", "None", 0, 0, 1, "no", 500, "Chômeur")
            cursor.execute('INSERT INTO tt_iso_card VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', new_user)
            connection.commit()
            await ctx.send(f"Bienvenue {ctx.author.mention}, dans l'aventure ISO land !")
        else:
            await ctx.send(f"{ctx.author.mention} Tu ne peux pas commencer l'aventure puisque tu es déjà inscrit...")
        connection.close()

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("start")