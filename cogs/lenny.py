import discord, random, json
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def lenny(self, ctx):
        a_file = open("no-move.json", "r")
        json_object_nm = json.load(a_file)
        a_file.close()
        await ctx.send(random.choice(json_object_nm['lenny']))

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("lenny")