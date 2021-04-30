import discord, sqlite3, asyncio
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="pollend", description="Terminer un sondage", options=[
                create_option(
                name="id_du_sondage",
                description="L'identifiant du sondage (qui est celui du sondage envoyé par le bot)",
                option_type=3,
                required=True
                )
                ])
    async def _pollend(self, ctx, id_du_sondage: str):
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        try:
            id_du_sondage = int(id_du_sondage)
        except:
            pass
        id_du_sondage = (f"{id_du_sondage}",)
        cursor.execute('SELECT * FROM polls WHERE message_id = ?', id_du_sondage)
        poll_values = cursor.fetchone()
        if poll_values == None:
            await ctx.send(f"{ctx.author.mention} Désolé mais le sondage que tu recherches n'a pas été retrouvé... essaie de voir si tu as entré le bon identifiant, ou si le sondage n'a pas déjà été terminé :wink:")
        else:
            channel_to_find = self.bot.get_channel(poll_values[1])
            try:
                msg = await channel_to_find.fetch_message(poll_values[0])
            except:
                pass
            poll_title = poll_values[2]
            poll_arguments = poll_values[3].split("\n")
            n, bs_n, numbers = 0, "\n", ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
            for reaction in msg.reactions:
                poll_arguments[n] = str(poll_arguments[n]) + f" • x{int(reaction.count) - 1}"
                n += 1
            poll_arguments = bs_n.join(poll_arguments)
            embed = discord.Embed(title=f"{poll_title} (terminé)", description=ctx.author.mention)
            embed.add_field(name="** **", value=poll_arguments, inline=False)
            await msg.edit(embed=embed, content=None)
            message_id = (f"{msg.id}",)
            cursor.execute('DELETE FROM polls WHERE message_id = ?', message_id)
            connection.commit()
            msg = await ctx.send(":white_check_mark:")
            await asyncio.sleep(1)
            await msg.delete()
        connection.close()

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("pollend")