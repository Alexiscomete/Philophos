import discord, requests, json, krock32
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def decode(self, ctx, service = None, *, arg = None):
        s_slash = "/"
        if service == None or arg == None:
            await ctx.send("N'oublie pas un argument ! (Plus d'infos : **+help encode**)")
        else:
            services = ['binary', 'base64']
            if service in services:
                async with ctx.typing():
                    if service.lower() == services[0] or service.lower() == services[1]:
                        decode_api = requests.get(f"https://some-random-api.ml/{service.lower()}?decode={arg}").json()
                        decode_api = decode_api['text']
                    embed = discord.Embed(title=f"Décodeur {s_slash.join(services)} vers texte")
                    embed.add_field(name=f"Texte codé en {service} : ", value=arg, inline=False)
                    embed.add_field(name="Résultat en texte :", value=str(decode_api), inline=False)
                try:
                    await ctx.send(embed=embed)
                except discord.errors.HTTPException:
                    await ctx.send("La conversion n'a pas pu être envoyé car elle contenait plus de 1023 caractères... ce qui est la limite dans un envoi d'embed !")
            else:
                await ctx.send("Veuillez entrer un type d'écriture valide !")

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("decode")