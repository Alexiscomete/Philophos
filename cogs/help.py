import discord, asyncio, json, requests
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['h', 'aide'])
    async def help(self, ctx, arg = None):
        a_file = open("no-move.json", "r")
        json_object_nm = json.load(a_file)
        a_file.close()

        command_groups, command_groups_cut = [], []
        changelog_versions = requests.get(f"https://iso-land.org/api/amanager/changelog.json").json()
        changelog_list = list(changelog_versions['changelogs'])
        separateur = "` `"

        for key in json_object_nm['main_help_command']:
            key_w = key.split(" ")[1:][0]
            command_groups.append(key)
            command_groups_cut.append(key_w.lower())

        if arg == None:
            nombre_de_commandes_seen, nb_commands = 0, 0
            embed = discord.Embed(title=":information_source: Aide des commandes invoquée.", color=0x7f00ff)
            embed.add_field(name="Afficher la liste des commandes d'un groupe :", value=f"```{self.client.command_prefix}help [groupe]```", inline=False)
            for key in json_object_nm['main_help_command']:
                for element in json_object_nm['main_help_command'][str(key)]:
                    nb_commands += 1
                command_groups.append(key)
                nb_commandes_c = len(json_object_nm['main_help_command'][str(key)])
                if not ctx.author.guild_permissions.kick_members and key != "🛠️ Staff [ALPHA]":
                    for element in json_object_nm['main_help_command'][str(key)]:
                        nombre_de_commandes_seen += 1
                    if nb_commandes_c == 1:
                        embed.add_field(name=key, value=f"{nb_commandes_c} commande", inline=True)
                    else:
                        embed.add_field(name=key, value=f"{nb_commandes_c} commandes", inline=True)
                elif ctx.author.guild_permissions.kick_members:
                    for element in json_object_nm['main_help_command'][str(key)]:
                        nombre_de_commandes_seen += 1
                    if nb_commandes_c == 1:
                        embed.add_field(name=key, value=f"{nb_commandes_c} commande", inline=True)
                    else:
                        embed.add_field(name=key, value=f"{nb_commandes_c} commandes", inline=True)

            embed.add_field(name="** **", value="[Inviter le bot](https://iso-land.org/amanager) | [Rejoindre le serveur support](https://discord.gg/WamZS7CExw) | [Documentation](https://amanagerx.iso-land.org/)", inline=False)
            embed.set_footer(text=f"v{changelog_list[-1]} | Il y a {nb_commands} commandes (dont {nombre_de_commandes_seen} auxquelles tu as accès).")
            await ctx.send(embed=embed)

# Commandes "help" pour commandes
        else:
            if arg in json_object_nm['help_commands']:
                embed = discord.Embed(title=f":information_source: {arg} | Aide", color=0x00B2EE)
                embed.add_field(name="A quoi sert cette commande ?", value=json_object_nm['help_commands'][str(arg)][0], inline=False)
                embed.add_field(name="Syntaxe(s) :", value="```" + str(json_object_nm['help_commands'][str(arg)][1]) + "```", inline=False)
                if len(json_object_nm['help_commands'][str(arg)]) == 3:
                    embed.add_field(name="Exemple(s) :", value="```" + str(json_object_nm['help_commands'][str(arg)][2]) + "```", inline=False)
                embed.set_footer(text=f"N'oublie pas le préfixe du bot avant chaque commande, qui est : {self.client.command_prefix}")
                help_help_command = await ctx.send(embed=embed)
                if arg == "help" or arg == "h" or arg == "aide":
                    await asyncio.sleep(10)
                    await help_help_command.edit(content="https://media.tenor.co/images/8c409e6f39acc1bd796e8031747f19ad/tenor.gif\nTu demandes de l'aide pour avoir une aide ? <:kappa:743778116849106946>", embed=None)

            elif arg.lower() in command_groups_cut or arg.lower() == "jv":
                if arg.lower() == "jv":
                    h_com = "jeux-vidéos"
                else:
                    h_com = arg.lower()
                commands_listing = ""
                test = command_groups_cut.index(str(h_com))
                test = command_groups[test]
                for element in json_object_nm['main_help_command'][str(test)]:
                    commands_listing = str(commands_listing) + "\n" + str(element)
                commands_listing = "```" + str(commands_listing) + "```" + f"\n\nTu peux obtenir de l'aide sur une commande en faisant **{self.client.command_prefix}help [commande]** !"
                await ctx.send(commands_listing)
            else:
                await ctx.send(f"{ctx.author.mention} L'aide ou le groupe que tu recherches n'existe pas... ré-essaie :wink:\nPour voir la liste des groupes : **{self.client.command_prefix}help**")

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("help")