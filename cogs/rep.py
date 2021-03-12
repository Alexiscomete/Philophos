import discord, sqlite3
from discord.ext import commands
from discord.ext.commands import cooldown

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 21600, commands.BucketType.user) #21600s = 6h
    async def rep(self, ctx):
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()

        rep = ctx.message.content.split(" ")
        if len(rep) == 1:
            await ctx.send(f"{ctx.author.mention} N'oublie pas de mentionner la personne à qui donner un point de réputation !")
            ctx.command.reset_cooldown(ctx)
        elif len(rep) > 1:
            member = str(rep[1]).replace("<@",'').replace(">",'').replace("!",'')
            try:
                member = int(member)
            except ValueError:
                await ctx.send(f"{ctx.author.mention} Il faut mentionner, ou envoyer l'identifiant du membre pour que tu puisses donner un point de réputation !")
                ctx.command.reset_cooldown(ctx)
            try:
                member = await self.client.fetch_user(str(member))
            except discord.errors.HTTPException:
                await ctx.send(f"{ctx.author.mention} L'utilisateur recherché n'a pas été trouvé...")
                ctx.command.reset_cooldown(ctx)

            if member.bot != False:
                await ctx.send(f"{ctx.author.mention} Tu ne peux pas donner de points de réputation à un bot ! :robot:")
                ctx.command.reset_cooldown(ctx)
            if member.id == ctx.author.id:
                await ctx.send(f"{ctx.author.mention} Tu ne peux pas te donner de points de réputation... ça serait trop simple sinon :stuck_out_tongue_winking_eye:")
                ctx.command.reset_cooldown(ctx)
            if member.bot == False and member.id != ctx.author.id:
                member_id = (f"{member.id}",)
                cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
                if cursor.fetchone() == None:
                    await ctx.send(f"Désolé {ctx.author.mention}, mais la personne avec qui tu essaies de donner un point de réputation ne s'est pas inscrite à l'aventure ISO land... Tu peux, néanmoins, aller lui en parler, et lui dire que la commande pour commencer l'aventure est **{self.client.command_prefix}start** ! :wink:")
                    ctx.command.reset_cooldown(ctx)
                else:
                    cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
                    rep_points = cursor.fetchone()[1]
                    rep_points_new = int(rep_points) + 1
                    updated_user = (f"{rep_points_new}", f"{member.id}",)
                    cursor.execute('UPDATE tt_iso_card SET rep_points = ? WHERE user_id = ?', updated_user)
                    connection.commit()

                    await ctx.send(f":up: Un point de réputation a été donné à **{member.name}** !")

                    member_id = (f"{member.id}",)
                    cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
                    member_values = cursor.fetchone()
                    member_values_list = member_values[2]
                    rep_points_new = int(member_values[1])

                    if rep_points_new == 1:
                        achievement = "<:reputation_point:810240527941238835>"
                        if member_values != None and achievement not in member_values_list:
                            archi_list = str(member_values[2]) + f" {achievement}"
                            updated_user = (f"{archi_list}", f"{member.id}",)
                            cursor.execute('UPDATE tt_iso_card SET archi_list = ? WHERE user_id = ?', updated_user)
                            connection.commit()
                        await ctx.send(f"{member.mention} Tu as obtenu un nouvel achievement ! (Avoir 1 point de réputation)")

                    if rep_points_new == 10:
                        achievement = "<:super_reputation_point:813110474555523104>"
                        if member_values != None and achievement not in member_values_list:
                            archi_list = str(member_values[2]) + f" {achievement}"
                            updated_user = (f"{archi_list}", f"{member.id}",)
                            cursor.execute('UPDATE tt_iso_card SET archi_list = ? WHERE user_id = ?', updated_user)
                            connection.commit()
                        await ctx.send(f"{member.mention} Tu as obtenu un nouvel achievement ! (Avoir 10 points de réputation)")

                    if rep_points_new == 20:
                        achievement = "<:mega_reputation_point:813110974126620672>"
                        if member_values != None and achievement not in member_values_list:
                            archi_list = str(member_values[2]) + f" {achievement}"
                            updated_user = (f"{archi_list}", f"{member.id}",)
                            cursor.execute('UPDATE tt_iso_card SET archi_list = ? WHERE user_id = ?', updated_user)
                            connection.commit()
                        await ctx.send(f"{member.mention} Tu as obtenu un nouvel achievement ! (Avoir 20 points de réputation)")

                    if rep_points_new == 50:
                        achievement = "<:epic_reputation_point:813110094837055499>"
                        if member_values != None and achievement not in member_values_list:
                            archi_list = str(member_values[2]) + f" {achievement}"
                            updated_user = (f"{archi_list}", f"{member.id}",)
                            cursor.execute('UPDATE tt_iso_card SET archi_list = ? WHERE user_id = ?', updated_user)
                            connection.commit()
                        await ctx.send(f"{member.mention} Tu as obtenu un nouvel achievement ! (Avoir 50 points de réputation)")

                    if rep_points_new == 100:
                        achievement = "<:super_epic_reputation_point:813109537744879628>"
                        if member_values != None and achievement not in member_values_list:
                            archi_list = str(member_values[2]) + f" {achievement}"
                            updated_user = (f"{archi_list}", f"{member.id}",)
                            cursor.execute('UPDATE tt_iso_card SET archi_list = ? WHERE user_id = ?', updated_user)
                            connection.commit()
                        await ctx.send(f"{member.mention} Tu as obtenu un nouvel achievement ! (Avoir 100 points de réputation)")

                    if rep_points_new == 500:
                        achievement = "<:ultimate_reputation_point:813108493317308437>"
                        if member_values != None and achievement not in member_values_list:
                            archi_list = str(member_values[2]) + f" {achievement}"
                            updated_user = (f"{archi_list}", f"{member.id}",)
                            cursor.execute('UPDATE tt_iso_card SET archi_list = ? WHERE user_id = ?', updated_user)
                            connection.commit()
                        await ctx.send(f"{member.mention} Tu as obtenu un nouvel achievement ! (Avoir 500 points de réputation)")

                    if rep_points_new == 1000:
                        achievement = "<:god_reputation_point:813108493241417808>"
                        if member_values != None and achievement not in member_values_list:
                            archi_list = str(member_values[2]) + f" {achievement}"
                            updated_user = (f"{archi_list}", f"{member.id}",)
                            cursor.execute('UPDATE tt_iso_card SET archi_list = ? WHERE user_id = ?', updated_user)
                            connection.commit()
                        await ctx.send(f"{member.mention} Tu as obtenu un nouvel achievement ! (Avoir 1000 points de réputation)")

                    if rep_points_new == 5000:
                        achievement = "<a:rainbow_reputation_point:813118888987721769>"
                        if member_values != None and achievement not in member_values_list:
                            archi_list = str(member_values[2]) + f" {achievement}"
                            updated_user = (f"{archi_list}", f"{member.id}",)
                            cursor.execute('UPDATE tt_iso_card SET archi_list = ? WHERE user_id = ?', updated_user)
                            connection.commit()
                        await ctx.send(f"{member.mention} Tu as obtenu un nouvel achievement ! (Avoir 5000 points de réputation)")

        connection.close()

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("rep")