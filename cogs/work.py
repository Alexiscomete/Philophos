import discord, sqlite3, random
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 86400, commands.BucketType.member) #86400s = 24h
    @commands.command()
    async def work(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        author_id = (f"{ctx.author.id}",)
        cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', author_id)
        author_values = cursor.fetchone()
        if author_values == None:
            await ctx.send(f"{ctx.author.mention} Tu ne peux pas travailler car tu ne t'es pas inscrit•e à l'aventure ISO land ! (Pour qu'elle inscrive : **+start**)")
        else:
            argent_de_author = author_values[5]
            new_argent_author = argent_de_author + random.randint(x, y)
            updated_author = (f"{new_argent_author}", f"{ctx.author.id}",)
            cursor.execute('UPDATE tt_iso_card SET dailies = ? WHERE user_id = ?', updated_author)
            connection.commit()

            await ctx.send(f"{ctx.author.mention} Tu as bien travaillé aujourd'hui ! Ce qui te rapporte {new_argent_author}<:aCoin:813464075249123339> !")

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("work")