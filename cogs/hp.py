import discord, requests, json
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hp(self, ctx):
        espace, api_hypixel_achievements = ", ", []

        def number_separator(s):
            s = round(int(s))
            s = str(s)
            l = len(s)
            d = round(l / 3)
            for i in range(1,d+1):
                s = s[:l-3*i] + " " + s[l-3*i:]
            return s

        API_KEY_HYPIXEL = "c507846f-dae0-4adf-8cc0-cada20275f2d"
        hp_hypixel = ctx.message.content.split(" ")
        if len(hp_hypixel) == 1:
            await ctx.send(f"N'oublie pas d'arguments ! Plus d'infos : +help hp")
        else:
            if hp_hypixel[1] == "stats":
                try:
                    search_api = requests.get(f"https://minecraft-api.com/api/uuid/{espace.join(hp_hypixel[2:])}/json").json()
                    player = search_api['uuid']
                except json.decoder.JSONDecodeError:
                    player = hp_hypixel[2]
                hp_hypixel_api = requests.get(f"https://api.hypixel.net/player?key={API_KEY_HYPIXEL}&uuid={player}").json()
                if hp_hypixel_api['success'] == True:
                    async with ctx.channel.typing():
                        embed = discord.Embed(title="Informations à propos d'un joueur du serveur Hypixel.", color=0xffd700)
                        file = discord.File("/root/discord-bots/AmanagerX/images/hypixel_icon.jpg", filename="hypixel_icon.jpg")
                        embed.set_thumbnail(url="attachment://hypixel_icon.jpg")
                        embed.add_field(name="Pseudo du joueur", value=hp_hypixel_api['player']['displayname'], inline=True)
                        for element in hp_hypixel_api['player']['achievements']:
                            api_hypixel_achievements.append(f"{element} : {hp_hypixel_api['player']['achievements'][str(element)]}")
                        achievements_list = espace.join(api_hypixel_achievements)
                        if "achievementPoints" in hp_hypixel_api['player']:
                            nb_achievements_points = number_separator(hp_hypixel_api['player']['achievementPoints'])
                            embed.add_field(name="Achievements", value=f"{len(hp_hypixel_api['player']['achievements'])}\n{nb_achievements_points} pts", inline=True)
                        elif "achievementPoints" not in hp_hypixel_api['player']:
                            embed.add_field(name="Achievements", value=f"{len(hp_hypixel_api['player']['achievements'])}\n", inline=True)
                        if "coin" in hp_hypixel_api['player']['stats']['Arcade']:
                            nb_pieces = number_separator(hp_hypixel_api['player']['stats']['Arcade']['coins'])
                            embed.add_field(name="Pièces", value=nb_pieces, inline=True)
                        if "karma" in hp_hypixel_api['player']:
                            nb_karma = number_separator(hp_hypixel_api['player']['karma'])
                            embed.add_field(name="Karma", value=nb_karma, inline=True)
                        if "networkExp" in hp_hypixel_api['player']:
                            nb_experience = number_separator(hp_hypixel_api['player']['networkExp'])
                            embed.add_field(name="Expérience", value=nb_experience, inline=True)
                        embed.add_field(name="Dernier jeu auquel le joueur a été :", value=hp_hypixel_api['player']['mostRecentGameType'], inline=True)
                        embed.set_footer(text=f"Votre UUID est : {hp_hypixel_api['player']['uuid']}")
                    await ctx.send(file=file, embed=embed)
                else:
                    await ctx.send("L'UUID entré n'est pas correct.")

            elif hp_hypixel[1] == "bans":
                hp_hypixel_api = requests.get("https://api.hypixel.net/watchdogstats?key=c507846f-dae0-4adf-8cc0-cada20275f2d").json()
                embed = discord.Embed(title="Informations sur les bannissements du serveur Hypixel.", color=0xffd700)
                file = discord.File("/root/discord-bots/AmanagerX/images/hypixel_icon.jpg", filename="hypixel_icon.jpg")
                embed.set_thumbnail(url="attachment://hypixel_icon.jpg")
                watchdog_lastminute = number_separator(str(hp_hypixel_api['watchdog_lastMinute']))
                staff_daily = number_separator(str(hp_hypixel_api['staff_rollingDaily']))
                watchdog_daily = number_separator(str(hp_hypixel_api['watchdog_rollingDaily']))
                staff_total = number_separator(str(hp_hypixel_api['staff_total']))
                watchdog_total = number_separator(str(hp_hypixel_api['watchdog_total']))
                total_bans = number_separator(str(hp_hypixel_api['watchdog_total'] + hp_hypixel_api['staff_total']))
                embed.add_field(name="Nombre de bans depuis une minute :", value=watchdog_lastminute, inline=False)
                embed.add_field(name="Nombre de bans/jour par le staff :", value=staff_daily, inline=False)
                embed.add_field(name="Nombre de bans/jour automatiques :", value=watchdog_daily, inline=False)
                embed.add_field(name="Total des bans du staff :", value=staff_total, inline=False)
                embed.add_field(name="Total des bans automatiques :", value=watchdog_total, inline=False)
                embed.add_field(name="Total de bans comptabilisés :", value=total_bans, inline=False)                    
                await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("hp")