import discord, sqlite3, asyncio
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def give(self, ctx, member: discord.Member = None, argent: int = None):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        if member == None or argent == None:
            await ctx.send(f"{ctx.author.mention} N'oublie pas de choisir un membre à qui donner de l'argent et le montant !")
        else:
            if member.bot == True:
                await ctx.send(f"{ctx.author.mention} Tu ne peux pas donner d'argent aux bots... :wink:")
            if member.bot == False:
                if member == ctx.author:
                    await ctx.send("Tu ne peux pas te donner de l'argent à toi-même ! :stuck_out_tongue:")
                else:
                    member_id = (f"{member.id}",)
                    cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
                    member_values = cursor.fetchone()
                    author_id = (f"{ctx.author.id}",)
                    cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', author_id)
                    author_values = cursor.fetchone()
                    if member_values == None:
                        await ctx.send(f"{ctx.author.mention} Tu ne peux pas donner d'argent à cette personne car elle ne s'est pas inscrite à l'aventure ISO land ! (Pour qu'elle inscrive : **{self.client.command_prefix}start**)")
                    else:
                        argent_de_author = author_values[5]
                        if argent > argent_de_author:
                            await ctx.send(f"{ctx.author.mention} Tu ne peux pas donner autant d'argent car tu n'en as pas assez sur ta carte !")
                        else:
                            if argent < 1:
                                await ctx.send(f"{ctx.author.mention} Tu ne peux pas effectuer cette transaction car le montant est trop bas (minimum 1<:aCoin:813464075249123339>) !")
                            else:
                                transac_give = await ctx.send(f"{ctx.author.mention} Es-tu sûr de vouloir effectuer cette transaction ?\nRéponds **oui** ou **non**, tu as 15 secondes.")
                                try:
                                    msg = await self.client.wait_for("message", check=check, timeout=15)
                                except asyncio.TimeoutError:
                                    await transac_give.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                                await msg.delete()
                                choice = msg.content.lower()
                                if choice == "non":
                                    await transac_give.edit(embed=None, content=":x: Annulation de la transaction !")
                                elif choice == "oui":
                                    await transac_give.edit(embed=None, content=f"<a:hourglass_loading:817441643644583956> Transaction en cours...")
                                    argent_a_donner = argent
                                    ancient_argent_author = argent_de_author
                                    taxe = argent*0.02 # le complément est la taxe de 2%
                                    new_argent_author = argent_de_author - argent_a_donner - taxe
                                    new_argent_author = round(new_argent_author, 2)

                                    ancient_argent_member = member_values[5]
                                    new_argent_member = ancient_argent_member + argent_a_donner

                                    updated_author = (f"{new_argent_author}", f"{ctx.author.id}",)
                                    cursor.execute('UPDATE tt_iso_card SET dailies = ? WHERE user_id = ?', updated_author)
                                    updated_member = (f"{new_argent_member}", f"{member.id}",)
                                    cursor.execute('UPDATE tt_iso_card SET dailies = ? WHERE user_id = ?', updated_member)
                                    connection.commit()

                                    await asyncio.sleep(2)
                                    await transac_give.edit(embed=None, content=f"**Transaction** effectuée par : {ctx.author.mention}\ncréditeur : {member.mention}\nMontant : {argent_a_donner}<:aCoin:813464075249123339> (Montant total : {argent_a_donner + taxe}<:aCoin:813464075249123339>)\nTaxe : {taxe}<:aCoin:813464075249123339> (2%)")

                                else:
                                    await transac_give.edit(embed=None, content="Une erreur est survenue... ré-essaie ! :wink:")

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("give")