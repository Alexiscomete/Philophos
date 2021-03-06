import discord, asyncio, random, string
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pwd(self, ctx):
        espace = " "
        pwd = ctx.message.content.split(" ")
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        def password_gen(pwd_nb_caracteres, is_numbers, is_caracters):
            pas_espace = ""
            pwd_list = []
            pwd_caracters = [',', ':', ';', '-', '+', '(', ')', '@', '*', '#', '€', '%', '&', '/', '_', '~', '`', '|', '°', '=', '{', '}', '[', ']', '<', '>']
            for i in range(pwd_nb_caracteres):
                random_number = random.randint(1,4)
                if random_number == 1:
                    pwd_list.append(random.choice(list(string.ascii_lowercase)))
                elif random_number == 2:
                    pwd_list.append(random.choice(list(string.ascii_uppercase)))
                elif random_number == 3:
                    if is_numbers.lower() == "oui":
                        pwd_list.append(str(random.randint(0,9)))
                    else:
                        random_number_2 = random.randint(1,2)
                        if random_number_2 == 1:
                            pwd_list.append(random.choice(list(string.ascii_lowercase)))
                        else:
                            pwd_list.append(random.choice(list(string.ascii_uppercase)))
                elif random_number == 4:
                    if is_caracters.lower() == "oui":
                        pwd_list.append(random.choice(pwd_caracters))
                    else:
                        random_number_2 = random.randint(1,2)
                        if random_number_2 == 1:
                            pwd_list.append(random.choice(list(string.ascii_lowercase)))
                        else:
                            pwd_list.append(random.choice(list(string.ascii_uppercase)))
            password = pas_espace.join(pwd_list)
            return password
        pwd_bot_message = await ctx.send(f"{ctx.author.mention} Bienvenue sur le générateur de mot de passe d'Amanager !")
        await asyncio.sleep(2)
        await pwd_bot_message.edit(content=f"{ctx.author.mention} Tu veux combien de caractères ? (entre 8 et 128)")
        try:
            msg = await self.client.wait_for("message", check=check, timeout=10)
        except asyncio.TimeoutError:
            await pwd_bot_message.edit(content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
        try:
            pwd_nb_caracteres = int(msg.content)
        except ValueError:
            await pwd_bot_message.edit(content=f"{ctx.author.mention} Vous n'avez pas entré de nombre...")
        if pwd_nb_caracteres > 128 or pwd_nb_caracteres < 8:
            await pwd_bot_message.edit(content=f"{ctx.author.mention} Votre nombre n'est pas valide... (Il est trop grand ou trop petit.)")
        else:
            await msg.delete()
            await pwd_bot_message.edit(content=f"{ctx.author.mention} Veux-tu y inclure des chiffres ? (oui ou non)")
            try:
                msg = await self.client.wait_for("message", check=check, timeout=10)
            except asyncio.TimeoutError:
                await pwd_bot_message.edit(content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
            if msg.content.lower() != "oui" and msg.content.lower() != "non":
                await pwd_bot_message.edit(content="Vous n'avez pas entré de réponse valable... (oui OU non)")
            elif msg.content.lower() == "oui" or msg.content.lower() == "non":
                is_numbers = msg.content
                await msg.delete()
                await pwd_bot_message.edit(content=f"{ctx.author.mention} Veux-tu y inclure des caractères spéciaux ? (oui ou non)")
                try:
                    msg = await self.client.wait_for("message", check=check, timeout=10)
                except asyncio.TimeoutError:
                    await pwd_bot_message.edit(content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                if msg.content.lower() != "oui" and msg.content.lower() != "non":
                    await pwd_bot_message.edit(content="Vous n'avez pas entré de réponse valable... (oui OU non)")
                elif msg.content.lower() == "oui" or msg.content.lower() == "non":
                    is_caracters = msg.content
                    await msg.delete()
                password = password_gen(pwd_nb_caracteres, is_numbers, is_caracters)
                await ctx.message.delete()
                await pwd_bot_message.edit(content=f"{ctx.author.mention} Ton mot de passe a été envoyé en MP !")
                await ctx.author.send(f"Vous aviez demandé un mot de passe :\n\n```{password}```")
                await asyncio.sleep(3)
                await pwd_bot_message.delete()

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("pwd")