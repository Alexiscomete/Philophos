import discord, sqlite3
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="start", description="T'inscrire à l'aventure ISO land !")
    async def _start(self, ctx):
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        member_id = (f"{ctx.author.id}",)
        cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
        if cursor.fetchone() == None:
            new_user = (ctx.author.id, 0, ".", "Je suis un nouveau dans l'aventure d'ISO land !", "None", 0, "Chômeur", 10, "🍪")
            cursor.execute('INSERT INTO tt_iso_card VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', new_user)
            connection.commit()
            new_user_2 = (ctx.author.id, ":beginner:", "")
            cursor.execute('INSERT INTO achievements VALUES(?, ?, ?)', new_user_2)
            connection.commit()
            await ctx.send(f"Bienvenue {ctx.author.mention}, dans l'aventure ISO land !")

        else:
            await ctx.send(f"{ctx.author.mention} Tu ne peux pas commencer l'aventure puisque tu y es déjà inscrit...")
        connection.close()

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("start")