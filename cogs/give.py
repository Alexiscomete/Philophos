import discord, sqlite3, asyncio
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="give", description="Donner des crédits à quelqu'un qui est inscrit à l'aventure ISO land !", options=[
                create_option(
                name="membre",
                description="Membre de discord à qui donner des crédits",
                option_type=6,
                required=True
                ),
                create_option(
                name="argent",
                description="Montant de crédits à donner (avec une taxe de 2%)",
                option_type=4,
                required=True
                )])
    async def _give(self, ctx, membre: discord.Member, argent: int):
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        if membre.bot == True:
            await ctx.send(f"{ctx.author.mention} Tu ne peux pas donner d'argent aux bots... :wink:")
        if membre.bot == False:
            if membre == ctx.author:
                await ctx.send("Tu ne peux pas te donner de l'argent à toi-même ! :stuck_out_tongue:")
            else:
                member_id = (f"{membre.id}",)
                cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
                member_values = cursor.fetchone()
                author_id = (f"{ctx.author.id}",)
                cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', author_id)
                author_values = cursor.fetchone()
                if member_values == None:
                    await ctx.send(f"{ctx.author.mention} Tu ne peux pas donner d'argent à cette personne car elle ne s'est pas inscrite à l'aventure ISO land ! (Pour qu'elle inscrive : **/start**)")
                elif author_values == None:
                    await ctx.send(f"{ctx.author.mention} Tu ne peux pas donner d'argent car tu ne t'es pas inscrit à l'aventure ISO land ! (Pour t'inscrire : **/start**)")
                else:
                    argent_de_author = author_values[5]
                    if argent > argent_de_author:
                        await ctx.send(f"{ctx.author.mention} Tu ne peux pas donner autant d'argent car tu n'en as pas assez sur ta carte !")
                    else:
                        if argent < 1:
                            await ctx.send(f"{ctx.author.mention} Tu ne peux pas effectuer cette transaction car le montant est trop bas (minimum 1<:aCoin:822427301488623620> ) !")
                        else:
                            argent_a_donner = argent
                            ancient_argent_author = argent_de_author
                            taxe = argent*0.02 # le complément est la taxe de 2%
                            new_argent_author = argent_de_author - argent_a_donner - taxe
                            new_argent_author = round(new_argent_author, 2)

                            ancient_argent_member = member_values[5]
                            new_argent_member = ancient_argent_member + argent_a_donner

                            updated_author = (f"{new_argent_author}", f"{ctx.author.id}",)
                            cursor.execute('UPDATE tt_iso_card SET dailies = ? WHERE user_id = ?', updated_author)
                            updated_member = (f"{new_argent_member}", f"{membre.id}",)
                            cursor.execute('UPDATE tt_iso_card SET dailies = ? WHERE user_id = ?', updated_member)
                            connection.commit()
                            await ctx.send(embed=None, content=f"**Transaction** effectuée par : {ctx.author.mention}\ncréditeur : {membre.mention}\nMontant : {argent_a_donner}<:aCoin:822427301488623620>  (Montant total : {argent_a_donner + taxe}<:aCoin:822427301488623620> )\nTaxe : {taxe}<:aCoin:822427301488623620>  (2%)")

        connection.close()

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("give")