import discord, sqlite3
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        server_id = (f"{member.guild.id}",)
        cursor.execute('SELECT * FROM bienvenue_au_revoir WHERE server_id = ?', server_id)
        server_values = cursor.fetchone()
        if server_values != None:
            is_activated_hello = server_values[3]
            if is_activated_hello == "yes":
                id_channel = int(server_values[5].replace("<#", "").replace(">", ""))
                message_to_send = server_values[1].replace("$$AUTHOR_MENTION$$", member.mention).replace("$$AUTHOR_NAME$$", member.name)
                channel_to_send = self.client.get_channel(id_channel)
                await channel_to_send.send(message_to_send)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        connection = sqlite3.connect("iso_card.db")
        cursor = connection.cursor()
        server_id = (f"{member.guild.id}",)
        cursor.execute('SELECT * FROM bienvenue_au_revoir WHERE server_id = ?', server_id)
        server_values = cursor.fetchone()
        if server_values != None:
            is_activated_goodbye = server_values[4]
            if is_activated_goodbye == "yes":
                id_channel = int(server_values[5].replace("<#", "").replace(">", ""))
                message_to_send = server_values[2].replace("$$AUTHOR_NAME$$", member.name)
                channel_to_send = self.client.get_channel(id_channel)
                await channel_to_send.send(message_to_send)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("hello_goodbye_messages")