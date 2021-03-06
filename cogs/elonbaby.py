import discord, random, string
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def elonbaby(self, ctx):
        lettres_accolees = ["Æ", "Œ"]
        symboles_maths = ["+", "-", "x", "÷"]
        await ctx.send(f"Prénom généré pour le bébé d'Elon Musk : {random.choice(string.ascii_uppercase)} {random.choice(lettres_accolees)} {random.choice(string.ascii_uppercase)} {random.choice(symboles_maths)} {random.randint(11,99)}")   

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("elonbaby")