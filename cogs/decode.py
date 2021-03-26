import discord, requests, json
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def decode(self, ctx, service = None, *, arg = None):
        s_slash = "/"
        if service == None or arg == None:
            await ctx.send(f"N'oublie pas un argument ! (Plus d'infos : **{self.client.command_prefix}help encode**)")
        else:
            services = ['binary', 'base64']
            if service in services:
                service = service.lower()
                if service == services[0] or service == services[1]:
                    pass
                    #decode_api = requests.get(f"https://some-random-api.ml/{service}?decode={arg}").json()
                    #decode_api = decode_api['text']
                embed = discord.Embed(title=f"Décodeur {s_slash.join(services)} vers texte")
                embed.add_field(name=f"Texte codé en {service} : ", value=arg, inline=False)
                embed.add_field(name="Résultat en texte :", value="bientôt de retour...", inline=False)
                try:
                    await ctx.send(embed=embed)
                except discord.errors.HTTPException:
                    await ctx.send("La conversion n'a pas pu être envoyé car elle contenait plus de 1023 caractères... ce qui est la limite dans un envoi d'embed !")
            else:
                await ctx.send("S'il te plaît, entre un type d'écriture valide !")

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("decode")