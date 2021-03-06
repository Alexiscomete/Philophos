import discord
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        APOD_channels = [771486705088856094, 611230647343644682] #apod-every-day (iso land) & apod (project garmana)
        if message and message.channel.id in APOD_channels:
            default_emojis = ["\N{OK HAND SIGN}", "\N{SMILING FACE WITH HEART-SHAPED EYES}", "\N{GRINNING FACE WITH STAR EYES}"]
            async def react_apod(message):
                for emoji in default_emojis:
                    await message.add_reaction(emoji)
            await react_apod(message)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("automations")