import discord
import json
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

class EmbedHelper():
    @staticmethod
    def get_help_message():
        embed_help = discord.Embed(title = 'Wangy Help')
        embed_help.add_field(
            name = '/wangy <tipe1|tipe2|tipe3> <name>',
            value = 'Menampilkan wangy wangy sesuai tipe',
            inline = False
        )
        embed_help.add_field(
            name = '/wangy <name>',
            value = 'Menampilkan wangy wangy tipe 1',
            inline = False
        )
        embed_help.add_field(
            name = '/wangy help',
            value = 'Menampilkan tata cara penggunaan',
            inline = False
        )
        return embed_help

class Logger():
    @staticmethod
    def initialize():
        logging.basicConfig(filename='logs/wangy.log', level=logging.INFO)

    @staticmethod
    def info(message):
        logging.info("{} -- {}".format(message, datetime.now()))

class WangyClient(discord.AutoShardedClient):
    def __init__(self):
        super(WangyClient, self).__init__(shard_count = int(os.getenv('DISCORD_SHARD_COUNT')))
        wangy_file = open('wangy.json',)
        self.wangy_string = json.load(wangy_file)

    async def on_ready(self):
        Logger.info("Bot started")

    async def on_guild_join(self, guild: discord.Guild):
        Logger.info("Guild join {}".format(guild.id))
        channels = guild.channels
        for channel in channels:
            if channel.name.lower() == 'general':
                embed_help = EmbedHelper.get_help_message()
                try:
                    await channel.send(embed = embed_help)
                except:
                    Logger.info("Error sending welcome message on guild {}".format(guild.id))

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        
        contents = message.content.split(" ")
        if contents[0] == "/wangy":
            if len(contents) == 2:
                if contents[1] == 'help':
                    Logger.info("Sending message (Type: help) (User: {})".format(message.author.id))
                    embed_help = EmbedHelper.get_help_message()
                    try:
                        await message.channel.send(embed = embed_help)
                    except Exception as err:
                        Logger.info("Error sending message (Type: help) (User: {}) (Reason: {})"
                            .format(message.author.id, err))
                else:
                    Logger.info("Sending message (Type: wangy_default) (User: {})".format(message.author.id))
                    wangy_text = self.wangy_string['wangy_1'].replace('$name', '**' + contents[1].upper() + '**')
                    try:
                        await message.channel.send(wangy_text)
                    except Exception as err:
                        Logger.info("Error sending message (Type: wangy_default) (User: {}) (Reason: {})"
                            .format(message.author.id, err))
            if len(contents) == 3:
                Logger.info("Sending message (Type: wangy_type) (User: {})".format(message.author.id))
                wangy_type = None
                if contents[1] == 'tipe1':
                    wangy_type = 'wangy_1'
                elif contents[1] == 'tipe2':
                    wangy_type = 'wangy_2'
                elif contents[1] == 'tipe3':
                    wangy_type = 'wangy_3'
                else:
                    Logger.info("Error sending message (Type: wangy_type) (User: {}) (Reason: wrong format)"
                        .format(message.author.id))
                    return
                
                wangy_text = self.wangy_string[wangy_type].replace('$name', '**' + contents[2].upper() + '**')
                try:
                    await message.channel.send(wangy_text)
                except Exception as err:
                    Logger.info("Error sending message (Type: wangy_type) (User: {}) (Reason: {})"
                            .format(message.author.id, err))

def main():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    Logger.initialize()
    Logger.info('App started')

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    client = WangyClient()
    client.run(TOKEN)

if __name__ == "__main__" :
    main()