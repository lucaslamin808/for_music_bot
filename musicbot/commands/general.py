import discord
from config import config
from discord.ext import commands
from discord.ext.commands import has_permissions
from musicbot import utils
from musicbot.audiocontroller import AudioController
from musicbot.utils import guild_to_audiocontroller, guild_to_settings

class General(commands.Cog):
    # Commandos geais de conexão do bot

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='connect', help=config.HELP_CONNECT, aliases=['c'])
    async def _connect(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        await audiocontroller.uconnect(ctx)

    @commands.command(name='disconnect', help=config.HELP_DISCONNECT, aliases=['dc'])
    async def _disconnect(self, ctx, guild=False):
        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        await audiocontroller.udisconnect()

    @commands.command(name='reset', help=config.HELP_DISCONNECT, aliases=['reiniciar', 'restart'])
    async def _reset(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        await current_guild.voice_client.disconnect(force=True)

        guild_to_audiocontroller[current_guild] = AudioController(
            self.bot, current_guild)
        await guild_to_audiocontroller[current_guild].register_voice_channel(ctx.author.voice.channel)

        await ctx.send("{} Conectado ao {}".format(":white_check_mark:", ctx.author.voice.channel.name))

    @commands.command(name='changechannel', help=config.HELP_CHANGECHANNEL, aliases=['cc'])
    async def _change_channel(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        vchannel = await utils.is_connected(ctx)
        if vchannel == ctx.author.voice.channel:
            await ctx.send("{} Já estou conectado ao canal: {}".format(":white_check_mark:", vchannel.name))
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        await current_guild.voice_client.disconnect(force=True)

        guild_to_audiocontroller[current_guild] = AudioController(
            self.bot, current_guild)
        await guild_to_audiocontroller[current_guild].register_voice_channel(ctx.author.voice.channel)

        await ctx.send("{} Movido para {}".format(":white_check_mark:", ctx.author.voice.channel.name))

    @commands.command(name='ping', help=config.HELP_PING)
    async def _ping(self, ctx):
        await ctx.send("Pong")

    @commands.command(name='setting', help=config.HELP_SETTINGS, aliases=['settings', 'set'])
    @has_permissions(administrator=True)
    async def _settings(self, ctx, *args):

        sett = guild_to_settings[ctx.guild]

        if len(args) == 0:
            await ctx.send(embed=await sett.format())
            return

        args_list = list(args)
        args_list.remove(args[0])

        response = await sett.write(args[0], " ".join(args_list), ctx)

        if response is None:
            await ctx.send("`Erro: Configurações não encontradas.`")
        elif response is True:
            await ctx.send("Configurações atualizadas!")

def setup(bot):
    bot.add_cog(General(bot))
