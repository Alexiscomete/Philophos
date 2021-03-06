import discord, requests
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def changelog(self, ctx, *, changelog_arg = None):
        changelog_versions = requests.get(f"https://iso-land.org/api/amanager/changelog.json").json()
        changelog_versions = changelog_versions['changelogs']

        espace = "\n"
        if changelog_arg == None:
            changelog_versions = espace.join(list(changelog_versions))
            embed = discord.Embed(title="Liste des versions de changelogs")
            embed.add_field(name="** **", value=changelog_versions, inline=False)
            await ctx.send(embed=embed)
        if changelog_arg.lower() != None:
            if changelog_arg.lower() not in changelog_versions:
                await ctx.send(f"La version que tu as entré n'est pas valide. Pour voir la liste des versions : **+changelog**.")
            else:
                cg = changelog_versions[f"{changelog_arg.lower()}"]
                embed = discord.Embed(title=f"Changelog • {changelog_arg.lower()}", color=0x666666)
                embed.add_field(name=cg['date'], value=cg['description'], inline=False)
                embed.set_footer(text="Les changelogs sont disponibles grâce à mon API, disponible ici : https://iso-land.org/api/")
                await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("changelog")