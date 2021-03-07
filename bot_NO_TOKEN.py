import discord, os, json, sqlite3, json
from discord.ext import commands

def get_prefix(bot, message):
    connection = sqlite3.connect("iso_card.db")
    cursor = connection.cursor()
    server_id = (f"{message.guild.id}",)
    cursor.execute('SELECT * FROM prefixes WHERE server_id = ?', server_id)
    server_values = cursor.fetchone()
    prefix = str(server_values[1])
    return prefix

intents = discord.Intents.all()
client = commands.Bot(command_prefix = '+', intents=intents)
client.remove_command('help')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        a_file = open("no-move.json", "r")
        json_object_nm = json.load(a_file)
        a_file.close()
        phrase_cooldown = json_object_nm['phrase_cooldown']
        await ctx.send(f"{ctx.author.mention} {phrase_cooldown}", delete_after=10)
        await ctx.message.delete()

@client.command()
async def load(ctx, *args):
    if ctx.author.id == 307092817942020096:
        cog_list, espace = [], " "
        for ext in args:
            cog_list.append(ext)
            client.load_extension(f"cogs.{ext}")
        await ctx.send(f"{espace.join(cog_list)} *ont été chargés !*")

@client.command()
async def unload(ctx, *args):
    if ctx.author.id == 307092817942020096:
        cog_list, espace = [], " "
        for ext in args:
            cog_list.append(ext)
            client.unload_extension(f"cogs.{ext}")
        await ctx.send(f"{espace.join(cog_list)} *ont été déchargés !*")

@client.command()
async def restart(ctx, *args):
    if ctx.author.id == 307092817942020096:
        cog_list, espace = [], " "
        for ext in args:
            cog_list.append(ext)
            client.reload_extension(f"cogs.{ext}")
        await ctx.send(f"{espace.join(cog_list)} *ont été rechargés !*")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('X')