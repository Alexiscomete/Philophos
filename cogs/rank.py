import discord, sqlite3
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="rank", description="Afficher ton niveau d'expérience, ou celui de quelqu'un d'autre, sur ce serveur !", options=[
                create_option(
                name="membre",
                description="Membre de discord",
                option_type=6,
                required=False
                )])
    async def _rank(self, ctx, membre: discord.Member = None):
        connection = sqlite3.connect("levels.db")
        cursor = connection.cursor()
        if membre == None:
            membre = ctx.author
        if membre.bot == True:
            await ctx.send(f"{ctx.author.mention} Les bots n'ont pas d'expérience... :wink:")
        if membre.bot == False:
            if membre.guild != ctx.guild:
                await ctx.send(f"{ctx.author.mention} Tu ne peux pas voir le niveau de ce membre car il n'est pas sur le même serveur que toi !")
            else:
                guild_name = "_" + str(ctx.guild.id)
                member_id = (f"{membre.id}",)
                cursor.execute('SELECT * FROM {} WHERE user_id = ?'.format(guild_name), member_id)
                member_values = cursor.fetchone()
                if member_values == None and membre != ctx.author:
                    await ctx.send(f"{ctx.author.mention} Une erreur est survenue... ré-essaie :wink:\nSi tu essaies de voir la carte de quelqu'un, il n'est sûrement pas enregistré ! (Il faut qu'il envoie un message sur un serveur où est le bot pour qu'il soit enregistré sur ce dit-serveur !).")
                elif member_values == None and membre == ctx.author:
                    await ctx.send(f"{ctx.author.mention} Renvoie la commande pour que l'activation de ton système d'XP s'effectue !")
                elif member_values != None:
                    exp = member_values[1]
                    level = int(member_values[2])
                    exp_goal = member_values[3]
                    if level == 100: level = ":infinity:"
                    embed = discord.Embed(title=f"Expérience de {membre.name}", description=membre.mention, color=0xf9c62d)
                    embed.add_field(name=":arrow_right: XP", value=exp_goal, inline=True)
                    embed.add_field(name=":large_orange_diamond: XP", value=exp, inline=True)
                    embed.add_field(name=":up: Niveau", value=level, inline=True)
                    await ctx.send(embed=embed)

        connection.close()

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("rank")