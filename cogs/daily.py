import discord, sqlite3
from discord.ext import commands
from discord.ext.commands import cooldown

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user) #86400s = 24h
    async def daily(self, ctx):
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()

        member_id = (f"{ctx.author.id}",)
        cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
        if cursor.fetchone() == None:
            await ctx.send(f"Tu ne peux pas récupérer ton argent quotidien car tu n'as pas commencé l'aventure ISO land ! (Pour débuter, fait : **{self.client.command_prefix}start**)")
            ctx.command.reset_cooldown(ctx)
        else:
            cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
            daily_points = cursor.fetchone()[5]
            daily_points_new = int(daily_points) + 100
            updated_user = (f"{daily_points_new}", f"{ctx.author.id}",)
            cursor.execute('UPDATE tt_iso_card SET dailies = ? WHERE user_id = ?', updated_user)
            connection.commit()

            await ctx.send(f"{ctx.author.mention} <:aCoin:822427301488623620>  Tu as reçu ton argent quotidien ! (100 crédits)")
        connection.close()

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("daily")