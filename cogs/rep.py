import discord, sqlite3
from discord.ext import commands
from discord.ext.commands import cooldown

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 21600, commands.BucketType.user) #21600s = 6h
    async def rep(self, ctx, member: discord.Member = None):
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()

        if member == None:
            await ctx.send(f"{ctx.author.mention} N'oublie pas de mentionner la personne à qui donner un point de réputation !")
            ctx.command.reset_cooldown(ctx)
        else:
            if member.bot != False:
                await ctx.send(f"{ctx.author.mention} Tu ne peux pas donner de points de réputation à un bot ! :robot:")
                ctx.command.reset_cooldown(ctx)
            if member.id == ctx.author.id:
                await ctx.send(f"{ctx.author.mention} Tu ne peux pas te donner de points de réputation... ça serait trop simple sinon :stuck_out_tongue_winking_eye:")
                ctx.command.reset_cooldown(ctx)
            if member.bot == False and member.id != ctx.author.id:
                member_id = (f"{member.id}",)
                cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
                if cursor.fetchone() == None:
                    await ctx.send(f"Désolé {ctx.author.mention}, mais la personne avec qui tu essaies de donner un point de réputation ne s'est pas inscrite à l'aventure ISO land... Tu peux, néanmoins, aller lui en parler, et lui dire que la commande pour commencer l'aventure est **{self.client.command_prefix}start** ! :wink:")
                    ctx.command.reset_cooldown(ctx)
                else:
                    cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
                    rep_points = cursor.fetchone()[1]
                    rep_points_new = int(rep_points) + 1
                    updated_user = (f"{rep_points_new}", f"{member.id}",)
                    cursor.execute('UPDATE tt_iso_card SET rep_points = ? WHERE user_id = ?', updated_user)
                    connection.commit()

                    await ctx.send(f":up: Un point de réputation a été donné à **{member.name}** !")

        connection.close()

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("rep")