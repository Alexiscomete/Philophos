import discord, sqlite3, json
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="achievement", description="Voir sa liste d'achivements, ou celle d'un utilisateur !", options=[
                create_option(
                name="membre",
                description="Membre de discord",
                option_type=6,
                required=False
                )])
    async def _achievement(self, ctx, membre: discord.Member = None):
        a_file = open("no-move.json", "r")
        json_object_nm = json.load(a_file)
        a_file.close()
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        if membre == None:
            membre = ctx.author
        member_id = (f"{membre.id}",)
        cursor.execute('SELECT * FROM achievements WHERE user_id = ?', member_id)
        member_values = cursor.fetchone()
        if member_values == None:
            if membre == ctx.author:
                await ctx.send(f"Tu ne peux pas afficher ta carte car tu n'as pas commencé l'aventure ISO land ! (Pour débuter, fait : **{self.client.command_prefix}start**)")
            else:
                await ctx.send(f"Tu ne peux pas afficher la carte de cette personne car elle ne s'est pas inscrite à l'aventure ISO land... (Elle peut débuter en faisant **{self.client.command_prefix}start**)")
        if member_values != None:
            a_misc = member_values[1] # succès divers
            a_reppoints = member_values[2] # succès des points de réputation
            len_a_misc = len(a_misc.split(" "))
            len_a_reppoints = len(a_reppoints.split(" "))
            all_a_misc = len(json_object_nm['achievements']['autres'])
            all_a_reppoints = len(json_object_nm['achievements']['reputation'])
            embed = discord.Embed(title=f"Succès de {membre.name}", description=membre.mention)
            if a_reppoints != "":
                embed.add_field(name=f"Points de réputation ({len_a_reppoints}/{all_a_reppoints})", value=a_reppoints, inline=False)
            if a_misc != "":
                embed.add_field(name=f"Divers ({len_a_misc}/{all_a_misc})", value=a_misc, inline=False)
            embed.set_footer(text="➡️ Pour voir ta aCard, fait /card !")
            await ctx.send(embed=embed)

        connection.close()

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("achievement")