import discord, sqlite3
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['inv'])
    async def inventory(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        member_id = (f"{member.id}",)
        cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
        member_values = cursor.fetchone()
        if member_values == None:
            if member == ctx.author:
                await ctx.send(f"{ctx.author.mention} Tu ne peux pas afficher ton inventaire car tu ne t'es pas inscrit à l'aventure ISO land... Pour t'inscrire, tu peux faire **{self.client.command_prefix}start** !")
            else:
                await ctx.send(f"{ctx.author.mention} Tu ne peux pas afficher l'inventaire de cette personne car elle ne s'est pas inscrite à l'aventure ISO land... Pour qu'elle s'inscrire, elle peut faire **{self.client.command_prefix}start** !")
        else:
            slots_max = member_values[7]
            inventory = member_values[8]
            slots_used = len(inventory.split(" "))
            embed = discord.Embed(title=f"Inventaire de {member.name} (bêta)", description=member.mention, color=0x000000)
            embed.add_field(name=f"Emplacements : {slots_used}/{slots_max}", value=inventory, inline=False)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("inventory")