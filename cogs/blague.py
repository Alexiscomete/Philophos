import discord, json, random
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def blague(self, ctx):
        a_file = open("no-move.json", "r")
        json_object_nm = json.load(a_file)
        a_file.close()
        if ctx.message.content == f"{self.client.command_prefix}blague":
            await ctx.send(random.choice(json_object_nm['blagues']))

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("blague")