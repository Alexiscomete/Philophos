import discord, os, json
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix = '+', intents=intents)
client.remove_command('help')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        a_file = open("no-move.json", "r")
        json_object_nm = json.load(a_file)
        a_file.close()

        #s = int(error.retry_after)
        #hours = s // 3600 
        #s = s - (hours * 3600)
        #minutes = s // 60
        #seconds = s - (minutes * 60)

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

client.run("NzYwMTcxODEzODY2NzAwODUw.X3ILKw.U0khIDApE1G1Z4lVmLQ8a6Wd0GY")