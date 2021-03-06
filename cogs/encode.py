import discord, requests, json, base64
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def encode(self, ctx, service = None, *, arg = None):
        s_slash = "/"
        if service == None or arg == None:
            await ctx.send("N'oublie pas un argument ! (Plus d'infos : **+help encode**)")
        else:
            services = ['binary', 'base64']
            if service in services:
                async with ctx.typing():
                    if service.lower() == services[0]:
                        encode_api = requests.get(f"https://some-random-api.ml/binary?text={arg}").json()
                        encode_api = encode_api[str(service.lower())]
                    elif service.lower() == services[1]:
                        encode_api = requests.get(f"https://some-random-api.ml/base64?encode={arg}").json()
                        encode_api = encode_api[str(service.lower())]
                    #embed = discord.Embed(title=f"Encodeur texte vers {s_slash.join(services)}")
                    #embed.add_field(name="Texte d'origine : ", value=arg, inline=False)
                    #embed.add_field(name=f"Résultat en {service} :", value=str(encode_api), inline=False)
                #try:
                #    await ctx.send(embed=embed)
                #except discord.errors.HTTPException:
                #    await ctx.send("La conversion n'a pas pu être envoyé car elle contenait plus de 1023 caractères... ce qui est la limite dans un envoi d'embed !")
            else:
                await ctx.send("Veuillez entrer un type d'écriture valide !")

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("encode")