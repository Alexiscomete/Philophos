import discord, random, TenGiphPy, sqlite3
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def karen(self, ctx):
        karen = ctx.message.content.split(" ")
        random_karen = random.randint(1, 4)
        if len(karen) == 2:
            karen_mentions_answers = [f"C'est toi la Karen de ce serveur ! {karen[1]}", f"{karen[1]} est entré en mode 'Karen' !", f"Vous voulez que j'appelle le manager, {karen[1]} ?"]
            await ctx.send(random.choice(karen_mentions_answers))
        else:
            if random_karen == 1: # joke
                jokes_karen = ['I want to speak to the manager !', 'I want to speak with the manager !', 'Take the kids out.', 'I have a complaint, i want to speak to the manager', f'{ctx.author.mention} entre en mode Karen !']
                await ctx.send(random.choice(jokes_karen))
            elif random_karen == 2: # meme (image)
                memes_karen = ['https://is.gd/NShcnL', 'https://is.gd/hY2B4H', 'https://is.gd/KG4vtc', 'https://is.gd/tBvPsH', 'https://is.gd/SG4WmK', 'https://is.gd/xzGV2u', 'https://is.gd/8yJPKU', 'https://is.gd/H2gMSh']
                await ctx.send(random.choice(memes_karen))
            elif random_karen == 3: # gif
                rgif = TenGiphPy.Tenor(token='88JQLKP3WXAI')
                karen_gif = rgif.random("karen")
                await ctx.send(karen_gif)
            elif random_karen == 4: # nouveau nickname
                try:
                    await ctx.author.edit(nick="Karen")
                except discord.errors.Forbidden:
                    if str(ctx.author.name) != str(ctx.guild.owner.name):
                        await ctx.channel.send("Je n'ai pas la permission de changer de pseudo... Donne moi cette permission pour que cette commande puisse fonctionner pleinement.\nSi j'ai déjà cette permission, vérifie que mon rôle soit le plus haut hiérarchiquement.")
                    elif str(ctx.author.name) == str(ctx.guild.owner.name):
                        await ctx.channel.send("Are you Queen Karen ?\nhttps://media.tenor.co/images/3f1fe20f669bff4e43fa862ee110b42d/tenor.gif")
                await ctx.message.delete()

        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        member_id = (f"{ctx.author.id}",)
        cursor.execute('SELECT * FROM tt_iso_card WHERE user_id = ?', member_id)
        achievement = "<:karen:791351537347723284>"
        member_values = cursor.fetchone()
        member_values_list = member_values[2]
        if member_values != None and achievement not in member_values_list:
            archi_list = str(member_values[2]) + f" {achievement}"
            updated_user = (f"{archi_list}", f"{ctx.author.id}",)
            cursor.execute('UPDATE tt_iso_card SET archi_list = ? WHERE user_id = ?', updated_user)
            connection.commit()
        connection.close()

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("karen")