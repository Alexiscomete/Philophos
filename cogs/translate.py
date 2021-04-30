import discord, requests, json
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="translate", description="Traduire un texte d'une langue à l'autre !.", options=[
                create_option(
                name="langue_de_départ",
                description="Langue du message à traduire.",
                option_type=3,
                required=True,
                choices=[
                create_choice(
                name="Anglais",
                value="en (Anglais)"
                ),
                create_choice(
                name="Chinois",
                value="zh (Chinois)"
                ),
                create_choice(
                name="Français",
                value="fr (Français)"
                ),
                create_choice(
                name="Allemand",
                value="de (Allemand)"
                ),
                create_choice(
                name="Hindi",
                value="hi (Hindi)"
                ),
                create_choice(
                name="Irlandais",
                value="ga (Irlandais)"
                ),
                create_choice(
                name="Italien",
                value="it (Italien)"
                ),
                create_choice(
                name="Japonais",
                value="ja (Japonais)"
                ),
                create_choice(
                name="Coréen",
                value="ko (Coréen)"
                ),
                create_choice(
                name="Portugais",
                value="pt (Portugais)"
                ),
                create_choice(
                name="Russe",
                value="ru (Russe)"
                ),
                create_choice(
                name="Espagnol",
                value="es (Espagnol)"
                )]),
                create_option(
                name="langue_de_fin",
                description="Langue dans laquelle le message sera traduit.",
                option_type=3,
                required=True,
                choices=[
                create_choice(
                name="Anglais",
                value="en (Anglais)"
                ),
                create_choice(
                name="Chinois",
                value="zh (Chinois)"
                ),
                create_choice(
                name="Français",
                value="fr (Français)"
                ),
                create_choice(
                name="Allemand",
                value="de (Allemand)"
                ),
                create_choice(
                name="Hindi",
                value="hi (Hindi)"
                ),
                create_choice(
                name="Irlandais",
                value="ga (Irlandais)"
                ),
                create_choice(
                name="Italien",
                value="it (Italien)"
                ),
                create_choice(
                name="Japonais",
                value="ja (Japonais)"
                ),
                create_choice(
                name="Coréen",
                value="ko (Coréen)"
                ),
                create_choice(
                name="Portugais",
                value="pt (Portugais)"
                ),
                create_choice(
                name="Russe",
                value="ru (Russe)"
                ),
                create_choice(
                name="Espagnol",
                value="es (Espagnol)"
                )]),
                create_option(
                name="message",
                description="Message à traduire.",
                option_type=3,
                required=True
                )])
    async def _translate(self, ctx, langue_de_départ: str, langue_de_fin: str, message: str):
        await ctx.defer()
        langue_de_départ_e = langue_de_départ.split(" ")[0]
        langue_de_fin_e = langue_de_fin.split(" ")[0]
        url = 'https://libretranslate.com/translate'
        languages = json.dumps({'q': f"{message}", 'source': f"{langue_de_départ_e}", 'target': f"{langue_de_fin_e}"})
        x = requests.post(url, data=languages, headers = {"Content-Type": "application/json"})
        resultat_de_fin = json.loads(x.text)
        resultat_de_fin = resultat_de_fin['translatedText']

        embed = discord.Embed(title="Traduction")
        embed.add_field(name=langue_de_départ, value=message, inline=False)
        embed.add_field(name=langue_de_fin, value=str(resultat_de_fin), inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("translate")