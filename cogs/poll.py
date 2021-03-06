import discord, sqlite3
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def poll(self, ctx, *, arg):
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        if arg.startswith("end"):
            arg_v = arg.split(" ")
            if len(arg_v) == 2:
                poll_id = (f"{arg_v[1]}",)
                cursor.execute('SELECT * FROM polls WHERE message_id = ?', poll_id)
                poll_values = cursor.fetchone()
                if poll_values == None:
                    await ctx.send(f"{ctx.author.mention} Désolé mais le sondage que tu recherches n'a pas été retrouvé... essayez de voir si tu as entré le bon identifiant, ou si le sondage n'est pas déjà terminé :wink:")
                else:
                    channel_to_find = self.client.get_channel(poll_values[1])
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
                    await ctx.message.delete()
        else:
            emote_reactions, n, bs_n, numbers, = [], 0, "\n", ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
            poll_message = arg.split(" / ")
            poll_title = poll_message[0]
            poll_message = poll_message[1:]

            if len(poll_message) < 2:
                await ctx.send(f"{ctx.author.mention} Ce sondage comporte moins de 2 éléments... Ré-essayez avec plus d'éléments.")
            if len(poll_message) > 10:
                await ctx.send(f"{ctx.author.mention} Ce sondage comporte plus de 10 éléments... Ré-essayez avec moins d'éléments.")
            else:
                for element in poll_message:
                    poll_message[n] = numbers[n] + " " + element
                    emote_reactions.append(str(numbers[n]))
                    n += 1
                embed = discord.Embed(title=poll_title, description=ctx.author.mention)
                embed.add_field(name="** **", value=f"{bs_n.join(poll_message)}", inline=False)
                embed.set_footer(text="ID du sondage = ID du message")
                poll_filled = await ctx.send(embed=embed)

                new_poll = (f"{poll_filled.id}", f"{poll_filled.channel.id}", f"{poll_title}", f"{bs_n.join(poll_message)}")
                cursor.execute('INSERT INTO polls VALUES(?, ?, ?, ?)', new_poll)
                connection.commit()

                async def react(message):
                    for emoji in emote_reactions:
                        await message.add_reaction(emoji)
                await react(poll_filled)
            await ctx.message.delete()

        connection.close()

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("poll")