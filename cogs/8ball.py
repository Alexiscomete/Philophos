import discord, random
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False and message.content.startswith("+8ball"):
            eight_ball = ["Oui !", "Non.", "Problablement.", "Probablement pas.", "Je ne sais pas..."]
            await message.channel.send(random.choice(eight_ball))

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("8ball")