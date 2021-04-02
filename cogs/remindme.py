import discord, asyncio
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="remindme", description="Voir la liste des versions du bot !", options=[
                create_option(
                name="temps",
                description="Temps avant lequel le rappel sera envoyé à l'utilisateur ! (Pour savoir la syntaxe : /help remindme)",
                option_type=3,
                required=True
                ),
                create_option(
                name="message",
                description="Message du rappel : c'est le motif.",
                option_type=3,
                required=True
                )])
    async def _remindme(self, ctx, temps: str, message: str):
        seconds, mef_time = 0, []
        temps = temps.split(" ")
        for element in temps:
            if "s" in element:
                seconds += int(element.replace("s", ""))
                mef_time.append(element.replace("s", " seconde(s)"))
            elif "m" in element:
                seconds += int(element.replace("m", "")) * 60
                mef_time.append(element.replace("m", " minute(s)"))
            elif "h" in element:
                seconds += int(element.replace("h", "")) * 3600
                mef_time.append(element.replace("h", " heure(s)"))
            elif "d" in element:
                seconds += int(element.replace("d", "")) * 86400
                mef_time.append(element.replace("d", " jour(s)"))

        if seconds < 300 or seconds > 604800:
            await ctx.send(f"{ctx.author.mention} Tu as définis une période invalide... (Le minimum étant de 5 minutes et le maximum de 7 jours.)")
        else:
            msg = await ctx.send(":white_check_mark:")
            await asyncio.sleep(1)
            await msg.delete()
            mef_time = ", ".join(mef_time)
            await ctx.author.send(f":pencil: **Ton rappel a bien été programmé ! Il se déclenchera dans : __{mef_time}__.**\n> {message}")
            await asyncio.sleep(seconds)
            await ctx.author.send(f":alarm_clock: C'est l'heure de ton rappel !\n> {message}")

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("remindme")