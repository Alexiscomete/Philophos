import discord, sqlite3, json
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="card", description="Voir ta carte, ou celle d'un utilisateur.", options=[
                create_option(
                name="membre",
                description="Membre de discord",
                option_type=6,
                required=False
                )])
    async def _card(self, ctx, membre: discord.Member = None):
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        if membre == None:
            membre = ctx.author
        if membre.bot == True:
            await ctx.send(f"{ctx.author.mention} Les bots n'ont pas de carte... :wink:")
        if membre.bot == False:
            a_file = open("no-move.json", "r")
            json_object_nm = json.load(a_file)
            a_file.close()
            member_id = (f"{membre.id}",)
            cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
            member_values = cursor.fetchone()
            if member_values == None:
                if membre == ctx.author:
                    await ctx.send(f"Tu ne peux pas afficher ta carte car tu n'as pas commencé l'aventure ISO land ! (Pour débuter, fait : **{self.client.command_prefix}start**)")
                else:
                    await ctx.send(f"Tu ne peux pas afficher la carte de cette personne car elle ne s'est pas inscrite à l'aventure ISO land... (Elle peut débuter en faisant **{self.client.command_prefix}start**)")
            else:
                rep_points = member_values[1] #member_values[0] = user_id
                archi_list = member_values[2]
                about_para = member_values[3]
                afk_status = member_values[4]
                daily = member_values[5]
                job = member_values[6]
                job_emoji = json_object_nm['jobs'][str(job)][2]

                if about_para == "":
                    about_para = "Je suis un nouveau dans l'aventure d'ISO land !"
                embed = discord.Embed(title=f"aCard de {membre.name}", description=membre.mention, color=0xf9c62d)
                embed.add_field(name="À propos", value=about_para, inline=False)
                if afk_status != "Nonei":
                    embed.add_field(name="Statut AFK", value=afk_status, inline=False)
                embed.add_field(name="<:0_reputation_point:822158196068188161> Point(s) de réputation", value=rep_points, inline=True)
                embed.add_field(name="<:aCoin:822427301488623620> Crédits", value=daily, inline=True)
                embed.add_field(name=f"{job_emoji} Travail (bêta)", value=job, inline=True)
                embed.set_footer(text="➡️  Pour voir ton inventaire, fait /inventory !\n➡️  Pour voir tes succès, fait /achievement !")
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("card")