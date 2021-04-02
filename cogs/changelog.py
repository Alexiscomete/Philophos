import discord, requests
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="changelog", description="Voir la liste des versions du bot !", options=[
                create_option(
                name="version",
                description="Version du bot, tu peux voir la liste des versions avec /changelog",
                option_type=3,
                required=False
                )])
    async def _changelog(self, ctx, version: str = None):
        changelog_versions = requests.get(f"https://iso-land.org/api/amanager/changelog.json").json()
        changelog_versions = changelog_versions['changelogs']

        espace = "\n"
        if version == None:
            changelog_versions = espace.join(list(changelog_versions))
            embed = discord.Embed(title="Liste des versions de changelogs")
            embed.add_field(name="** **", value=changelog_versions, inline=False)
            await ctx.send(embed=embed)
        else:
            if version.lower() not in changelog_versions:
                await ctx.send(f"La version que tu as entré n'est pas valide. Pour voir la liste des versions : **{self.client.command_prefix}changelog**.")
            else:
                cg = changelog_versions[f"{version.lower()}"]
                embed = discord.Embed(title=f"Changelog • {version.lower()}", description=cg['date'], color=0x666666)
                embed.set_footer(text="Les changelogs sont disponibles grâce à mon API, disponible ici : https://iso-land.org/api/")
                await ctx.send(embed=embed, content=cg['description'])

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("changelog")