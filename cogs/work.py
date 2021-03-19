import discord, sqlite3, random, json
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 86400, commands.BucketType.user) #86400s = 24h
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
            await ctx.send(f"{ctx.author.mention} Tu ne peux pas travailler car tu ne t'es pas inscrit à l'aventure ISO land ! (Pour qu'elle s'inscrive : **{self.client.command_prefix}start**)")
        else:
            argent_de_author = author_values[5]
            job = str(author_values[6])
            a_file = open("no-move.json", "r")
            json_object_nm = json.load(a_file)
            a_file.close()
            argent_limite = json_object_nm['jobs'][str(job)]
            a_min, a_max = int(argent_limite[0]), int(argent_limite[1])

            argent_a_ajouter = random.randint(a_min, a_max)
            new_argent_author = argent_de_author + argent_a_ajouter

            updated_author = (f"{new_argent_author}", f"{ctx.author.id}",)
            cursor.execute('UPDATE tt_iso_card SET dailies = ? WHERE user_id = ?', updated_author)
            connection.commit()

            if job == "Chômeur":
                await ctx.send(f"Tu es un chômeur {ctx.author.mention} ! Tu ne peux pas travailler pour l'instant... (mais bientôt :wink:)")
            else:
                await ctx.send(f"> {job}\n{ctx.author.mention} Tu as bien travaillé aujourd'hui ! Ce qui te rapporte {argent_a_ajouter}<:aCoin:822427301488623620>  !")

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("work")