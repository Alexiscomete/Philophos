import discord, asyncio
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def remindme(self, ctx, *, time = None):
        if time == None:
            await ctx.send(f"{ctx.author.mention} S'il te plaît, spécifie une durée pour ton rappel. (Plus d'infos : **{self.client.command_prefix}help remindme**)")
        else:
            seconds, mef_time = 0, []
            arg = time.split(" / ")
            time = arg[0].split(" ")
            if len(arg) == 1:
                await ctx.send(f"{ctx.author.mention} N'oublie pas de motif pour ton rappel !")
            else:
                motif = arg[1]
                for element in time:
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
                
                if seconds < 300:
                    await ctx.send(f"{ctx.author.mention} Tu as définis une trop petite période... (Le minimum étant de 5 minutes.)")
                elif seconds > 604800:
                    await ctx.send(f"{ctx.author.mention} Tu as définis une trop grande période... (Le maximum étant de 7 jours.)")
                else:
                    await ctx.message.delete()
                    mef_time = ", ".join(mef_time)
                    await ctx.author.send(f":pencil: **Ton rappel a bien été programmé ! Il se déclenchera dans : __{mef_time}__.**\n> {motif}")
                    await asyncio.sleep(seconds)
                    await ctx.author.send(f":alarm_clock: C'est l'heure de ton rappel !\n> {motif}")

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("remindme")