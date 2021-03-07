import discord, requests, json, urllib.request, base64
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def osu(self, ctx, reason = None, *, arg = None):
        a_file = open("no-move.json", "r")
        json_object_nm = json.load(a_file)
        a_file.close()
        osu_api_key = json_object_nm['token']['osu']
        if reason == None or arg == None:
            await ctx.send(f"{ctx.author.mention} N'oublie pas d'arguments ! (**user** ou **beatmap**, plus d'infos avec **{self.client.command_prefix}help osu** !)")
        elif reason == "user":
            async with ctx.typing():
                osu_user = requests.get(f"https://osu.ppy.sh/api/get_user?u={arg}&k={osu_api_key}").json()
                try:
                    osu_user = osu_user[0]
                except:
                    await ctx.send(f"{ctx.author.mention} Le joueur que tu recherches n'a pas été retrouvé... ré-essaye :wink: (**{self.client.command_prefix}help osu**)")

                secs = int(osu_user['total_seconds_played'])
                days = secs//86400
                hours = (secs - days*86400)//3600
                minutes = (secs - days*86400 - hours*3600)//60
                seconds = secs - days*86400 - hours*3600 - minutes*60
                country = osu_user['country']
                accuracy = round(float(osu_user['accuracy']), 2)
                level = round(float(osu_user['level']), 2)
                embed = discord.Embed(title=f"Profil osu! de {osu_user['username']}", description=osu_user['user_id'], color=0xff66aa)
                embed.add_field(name="Date d'inscription", value=osu_user['join_date'], inline=True)
                embed.add_field(name="Nombre de parties", value=osu_user['playcount'], inline=True)
                embed.add_field(name="Localisation", value=f":flag_{country.lower()}: " + str(country), inline=True)
                embed.add_field(name="Ranked score", value=osu_user['ranked_score'], inline=True)
                embed.add_field(name="Total score", value=osu_user['total_score'], inline=True)
                embed.add_field(name="PP rank", value=osu_user['pp_rank'], inline=True)
                embed.add_field(name="Niveau", value=level, inline=True)
                embed.add_field(name="Précision", value=accuracy, inline=True)
                embed.add_field(name="Temps joué", value=f"{days} jour(s), {hours} heure(s), {minutes} minute(s) et {seconds} seconde(s)", inline=True)
            await ctx.send(embed=embed)

        elif reason == "beatmap":
            async with ctx.typing():
                osu_map = requests.get(f"https://osu.ppy.sh//api/get_beatmaps?b={arg}&k={osu_api_key}").json()
                try:
                    osu_map = osu_map[0]
                except:
                    await ctx.send(f"{ctx.author.mention} La beatmap que tu recherches n'a pas été retrouvé... ré-essaye :wink: (**{self.client.command_prefix}help osu**)")
                seconds = int(osu_map['total_length'])
                seconds = seconds % (24 * 3600) 
                seconds %= 3600
                minutes = seconds // 60
                seconds %= 60
                mode = osu_map['mode']
                mode = json_object_nm['osu']['mode'][str(mode)]
                languages = osu_map['language_id']
                languages = json_object_nm['osu']['languages'][str(languages)]
                genres = osu_map['genre_id']
                genres = json_object_nm['osu']['genres'][str(genres)]
                embed = discord.Embed(title=f"Beatmap osu! : {osu_map['title']} — {osu_map['creator']}", description=f"ID : {osu_map['beatmap_id']} | Auteur de la beatmap : **{osu_map['creator']}**", color=0xff66aa)
                embed.add_field(name="Version", value=osu_map['version'], inline=True)
                embed.add_field(name="Mode", value=mode, inline=True)
                embed.add_field(name="Langue", value=languages, inline=True)
                embed.add_field(name="Genre", value=genres, inline=True)
                embed.add_field(name="Durée totale", value=f"{minutes} minute(s) et {seconds} seconde(s)", inline=True)
                embed.add_field(name="BPM", value=osu_map['bpm'], inline=True)
                embed.add_field(name="Difficulté", value=f"{osu_map['difficultyrating']} :star:", inline=True)
                embed.add_field(name="Nombre de cercles", value=osu_map['count_normal'], inline=True)
                embed.add_field(name="Nombre de sliders", value=osu_map['count_slider'], inline=True)
                embed.add_field(name="Nombre de spinners", value=osu_map['count_spinner'], inline=True)
                embed.add_field(name="Date d'upload", value=osu_map['submit_date'], inline=True)
                embed.add_field(name="Dernière update", value=osu_map['last_update'], inline=True)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("osu")