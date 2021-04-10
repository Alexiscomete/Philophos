import discord, sqlite3
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="inventory", description="Afficher ton inventaire, ou celui d'un utilisateur !", options=[
                create_option(
                name="membre",
                description="Choisis un utilisateur",
                option_type=6,
                required=False
                )])
    async def _inventory(self, ctx, membre: discord.Member = None):
        if membre == None:
            membre = ctx.author
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        member_id = (f"{membre.id}",)
        cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
        member_values = cursor.fetchone()
        if member_values == None:
            if membre == ctx.author:
                await ctx.send(f"{ctx.author.mention} Tu ne peux pas afficher ton inventaire car tu ne t'es pas inscrit à l'aventure ISO land... Pour t'inscrire, tu peux faire **/start** !")
            else:
                await ctx.send(f"{ctx.author.mention} Tu ne peux pas afficher l'inventaire de cette personne car elle ne s'est pas inscrite à l'aventure ISO land... Pour qu'elle s'inscrire, elle peut faire **/start** !")
        else:
            virgule = ", "
            inventory = member_values[8]
            slots_max = member_values[7]
            slots_used = len(inventory.split(" "))

            embed = discord.Embed(title=f"Inventaire de {membre.name} (bêta)", description=membre.mention, color=0x000000)
            embed.add_field(name=f"Basique : {slots_used}/{slots_max}", value=inventory, inline=False)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("inventory")