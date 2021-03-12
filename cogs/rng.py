import discord, random
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rng(self, ctx, nb1: int = None, nb2: int = None):
        if nb1 == None or nb2 == None:
            nb1, nb2 = 0, 100

        n_min, n_max = -4294967296, 4294967296
        if nb1 > nb2:
            await ctx.send(f"{ctx.author.mention} Le nombre 1 est plus grand que le nombre 2... relance la commande en faisant en sorte que le nombre 1 soit **plus petit** que le nombre 2.")
        elif nb1 < n_min or nb2 > n_max:
            await ctx.send(f"{ctx.author.mention} L'intervalle entrée est hors champ, la limite est de [{n_min} ; {n_max}] !")
        else:
            random_nb = random.randint(nb1, nb2)
            embed = discord.Embed(title=f"Générateur de nombres aléatoires")
            embed.add_field(name=f"Nombre généré : {random_nb}", value=f"Intervalle de valeurs : {nb1} et {nb2}")
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("rng")