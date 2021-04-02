import discord, sqlite3
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="poll", description="Créer et visualiser facilement un sondage !", options=[
                create_option(
                name="question",
                description="La question servira donner du contexte sur ton sondage, il sera en entête.",
                option_type=3,
                required=True
                ),
                create_option(
                name="Option_1",
                description="Les options proposées pour le sondage. (minimum 2, maximum 10)",
                option_type=3,
                required=True
                ),
                create_option(
                name="Option_2",
                description="Les options proposées pour le sondage. (minimum 2, maximum 10)",
                option_type=3,
                required=True
                ),
                create_option(
                name="Option_3",
                description="Les options proposées pour le sondage. (minimum 2, maximum 10)",
                option_type=3,
                required=False
                ),
                create_option(
                name="Option_4",
                description="Les options proposées pour le sondage. (minimum 2, maximum 10)",
                option_type=3,
                required=False
                ),
                create_option(
                name="Option_5",
                description="Les options proposées pour le sondage. (minimum 2, maximum 10)",
                option_type=3,
                required=False
                ),
                create_option(
                name="Option_6",
                description="Les options proposées pour le sondage. (minimum 2, maximum 10)",
                option_type=3,
                required=False
                ),
                create_option(
                name="Option_7",
                description="Les options proposées pour le sondage. (minimum 2, maximum 10)",
                option_type=3,
                required=False
                ),
                create_option(
                name="Option_8",
                description="Les options proposées pour le sondage. (minimum 2, maximum 10)",
                option_type=3,
                required=False
                ),
                create_option(
                name="Option_9",
                description="Les options proposées pour le sondage. (minimum 2, maximum 10)",
                option_type=3,
                required=False
                ),
                create_option(
                name="Option_10",
                description="Les options proposées pour le sondage. (minimum 2, maximum 10)",
                option_type=3,
                required=False
                )])
    async def _poll(self, ctx, question: str, Option_1: str, Option_2: str, Option_3: str = None, Option_4: str = None, Option_5: str = None, Option_6: str = None, Option_7: str = None, Option_8: str = None, Option_9: str = None, Option_10: str = None):
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        emote_reactions, n, bs_n, numbers, options, poll_message = [], 0, "\n", ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟'], [], []

        if Option_1 != None: options.append(Option_1)
        if Option_2 != None: options.append(Option_2)
        if Option_3 != None: options.append(Option_3)
        if Option_4 != None: options.append(Option_4)
        if Option_5 != None: options.append(Option_5)
        if Option_6 != None: options.append(Option_6)
        if Option_7 != None: options.append(Option_7)
        if Option_8 != None: options.append(Option_8)
        if Option_9 != None: options.append(Option_9)
        if Option_10 != None: options.append(Option_10)

        for element in options:
            poll_message.append(str(numbers[n] + " " + element))
            emote_reactions.append(str(numbers[n]))
            n += 1
        poll_arg = bs_n.join(poll_message)
        embed = discord.Embed(title=question, description=ctx.author.mention)
        embed.add_field(name="** **", value=poll_arg, inline=False)
        embed.set_footer(text="ID du sondage = ID du message")
        poll_filled = await ctx.send(embed=embed)

        new_poll = (f"{poll_filled.id}", f"{poll_filled.channel.id}", f"{question}", f"{poll_arg}")
        cursor.execute('INSERT INTO polls VALUES(?, ?, ?, ?)', new_poll)
        connection.commit()

        async def react(message):
            for emoji in emote_reactions:
                await message.add_reaction(emoji)
        await react(poll_filled)

        connection.close()

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("poll")