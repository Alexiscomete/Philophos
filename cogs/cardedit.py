import discord, sqlite3, json
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="cardedit", description="Editer sa carte.",
                options=[
                create_option(
                name="section",
                description="Section de la carte à modifier (voir choix)",
                option_type=3,
                required=True,
                choices=[
                    create_choice(
                    name="À propos",
                    value="1"
                    ),
                    create_choice(
                    name="AFK",
                    value="2"
                    ),
                    ]),
                create_option(
                name="message",
                description="Message à afficher dans la section 'à propos' ou dans ton statut AFK.",
                option_type=3,
                required=True
                )])
    async def _cardedit(self, ctx, section: str, message: str):
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        member_id = (f"{ctx.author.id}",)
        cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
        author_values = cursor.fetchone()
        if author_values == None:
            await ctx.send(f"Tu ne peux pas éditer ta carte car tu n'as pas commencé l'aventure ISO land ! (Pour débuter, fait : **/start**)")
        else:
            limite_caracteres = 100
            if len(list(message)) > limite_caracteres:
                await ctx.send(f"{ctx.author.mention} Ce statut ne peut pas être validé car il dépasse la limite de {limite_caracteres} caractères.")
            else:
                if section == "1":
                    member_id = (f"{ctx.author.id}",)
                    cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
                    updated_user = (f"{message}", f"{ctx.author.id}",)
                    cursor.execute('UPDATE tt_iso_card SET about = ? WHERE user_id = ?', updated_user)
                    connection.commit()
                    embed = discord.Embed(description=message)
                    await ctx.send(embed=embed, content="Le contenu **à propos** de ta carte a bien été actualisé !")
                elif section == "2":
                    member_id = (f"{ctx.author.id}",)
                    cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
                    updated_user = (f"{message}", f"{ctx.author.id}",)
                    cursor.execute('UPDATE tt_iso_card SET afk = ? WHERE user_id = ?', updated_user)
                    connection.commit()
                    embed = discord.Embed(description=message)
                    await ctx.send(embed=embed, content="Ton statut AFK a bien été enregistré !")

        connection.close()
    
    @commands.Cog.listener()
    async def on_message(self, message):
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        member_id = (f"{message.author.id}",)
        cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
        author_values_2 = cursor.fetchone()
        if author_values_2 != None:
            is_afk = author_values_2[4]
            if message and not message.content.startswith(f"/cardedit") and message.author.bot == False and is_afk != "Nonei":
                updated_user = ("Nonei", f"{message.author.id}",)
                cursor.execute('UPDATE tt_iso_card SET afk = ? WHERE user_id = ?', updated_user)
                connection.commit()
                #await message.channel.send(f"{message.author.mention} Tu es de retour ! Ton statut AFK a donc été désactivé.", delete_after=10)

        if message and not message.content.startswith(f"/cardedit") and not message.content.startswith(f"/card") and message.author.bot == False:
            for user in message.mentions:
                member_id = (f"{user.id}",)
                cursor.execute('SELECT afk FROM tt_iso_card WHERE user_id = ?', member_id)
                user_afk_s = cursor.fetchone()
                #if user_afk_s == None:
                #    await message.channel.send(f"{message.author.mention} Désolé mais l'utilisateur ({user.name}) que tu as mentionné est actuellement en AFK. Voici le statut qu'il/elle a laissé :\n> {user_afk_s[4]}")

        connection.close()

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("cardedit")