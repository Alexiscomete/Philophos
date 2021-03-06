import discord, json, requests, random
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def shorten(self, ctx):
        espace = " "
        shorten = ctx.message.content.split(" ")
        if len(shorten) == 1:
            await ctx.send("N'oublie pas de spécifier le lien que tu veux raccourcir !")
        elif len(shorten) > 1:
            async with ctx.channel.typing():
                if len(shorten) == 2:
                    shorten_services = ['rebrand.ly', 'is.gd', 'v.gd', 'urlz']
                    service_used = random.choice(shorten_services)
                    long_link = shorten[1]
                elif len(shorten) == 3:
                    service_used = shorten[1]
                    long_link = shorten[2]

                if "https://" not in long_link:
                    long_link = "https://" + long_link

                if service_used == "rebrand.ly":
                    linkRequest = {
                    "destination": long_link,
                    "domain": { "fullName": "rebrand.ly" }
                    }
                    requestHeaders = {
                        "Content-type": "application/json",
                        "apikey": "00d84bd68866452291f26e6dd0d5c82a",
                    }
                    r = requests.post("https://api.rebrandly.com/v1/links",
                        data = json.dumps(linkRequest),
                        headers=requestHeaders)
                    if (r.status_code == requests.codes.ok):
                        link = r.json()
                        new_link = link['shortUrl']
                        service = "rebrand.ly"

                    else:
                        await ctx.send(f"{ctx.author.mention} Il y a eu une erreur... votre lien n'est pas valide. (Si le lien est valide, vérifie si tu n'as pas oublié 'https://' au début du lien.)")
                elif service_used == "is.gd": #is.gd
                    service = "is.gd"
                    isgd = requests.get(f"https://is.gd/create.php?format=json&url={long_link}").json()
                    try:
                        new_link = isgd['shorturl']
                    except KeyError:
                        await ctx.send(f"{ctx.author.mention} Le lien n'a pas pu être généré... vérifie si ton lien est accessible.")
                elif service_used == "v.gd": #v.gd
                    service = "v.gd"
                    vgd = requests.get(f"https://v.gd/create.php?format=json&url={long_link}").json()

                    try:
                        new_link = vgd['shorturl']
                    except KeyError:
                        await ctx.send(f"{ctx.author.mention} Le lien n'a pas pu être généré... vérifie si ton lien est accessible.")
                elif service_used == "urlz": #urlz
                    service = "urlz"
                    urlz_service = requests.get(f"https://urlz.fr/api_new.php?url={long_link}")
                    new_link = urlz_service.text

                else:
                    await ctx.send(f"Entre un service valide ! (Plus d'infos : **+help shorten**)")

                embed = discord.Embed(title=f"+shorten <service> [lien]")
                embed.add_field(name="Lien d'origine :", value=f"{long_link}", inline=False)
                embed.add_field(name="Lien raccourci :", value=f"{new_link}", inline=False)
                embed.set_footer(text=f"Service utilisé : {service}")
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("shorten")