import discord, random
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def mcachievement(self, ctx, *, achievement = None):
        espace_web = "%20"
        achievement_l = achievement.split(" ")
        if achievement == None:
            await ctx.send(f"N'oublie pas d'arguments ! (numéro de la couleur, puis message : pour plus d'aide => **{self.client.command_prefix}help achievement)**")
        else:
            try:
                color = int(achievement_l[0])
                message_sent = espace_web.join(achievement_l[1:])
            except ValueError:
                color = random.randint(1,39)
                message_sent = achievement
            message_sent = message_sent.replace("?", "")
            if color < 1 or color > 39:
                await ctx.send(f"Le numéro de la couleur entrée n'est pas valide ! Il doit être compris entre 1 et 39. (Si tu veux voir la liste des numéros de couleur : **{self.client.command_prefix}help achievement**)")
            else:
                await ctx.send(f"https://minecraftskinstealer.com/achievement/{color}/Achievement%20get!/{message_sent}")

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("mcachievement")