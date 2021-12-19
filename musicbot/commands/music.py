import asyncio
import discord
import aiohttp
from lyrics_extractor import SongLyrics
from config import config
from discord.ext import commands
from musicbot import linkutils, utils
import typing as t
import datetime as dt

class Music(commands.Cog):
    """ Todos os comandos relacionados a reprodução de músicas

            - execução de comandos"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", alisases=['ajuda', 'h'], help=config.HELP_HELP)
    async def help(self,ctx):
        helptxt = ''
        # se for criar novos comandos certifique-se de passar um arg de help
        for command in self.bot.commands:
            helptxt += f'**{command}** - {command.help}\n' 
        embedhelp = discord.Embed(
            colour = config.EMBED_COLOR,
            title=f'Comandos do {self.bot.user.name}',
            description = helptxt
        )
        embedhelp.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=embedhelp)
        
    @commands.command(name='play', help=config.HELP_YT, aliases=['p'])
    async def _play_song(self, ctx, *, track: str):

        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if(await utils.is_connected(ctx) == None):
            if await audiocontroller.uconnect(ctx) == False:
                return

        if track.isspace() or not track:
            return

        if await utils.play_check(ctx) == False:
            return

        # redefine o timer
        audiocontroller.timer.cancel()
        audiocontroller.timer = utils.Timer(audiocontroller.timeout_handler)

        if audiocontroller.playlist.loop == True:
            embedvc = discord.Embed(
                colour= config.EMBED_COLOR,
                description = "O Loop está ativado Use {}loop para desativá-lo".format(config.BOT_PREFIX)
            )
            await ctx.send(embed=embedvc)
            return

        song = await audiocontroller.process_song(track)

        if song is None:
            await ctx.send(config.SONGINFO_ERROR)
            return

        if song.origin == linkutils.Origins.Default:

            if audiocontroller.current_song != None and len(audiocontroller.playlist.playque) == 0:
                await ctx.send(embed=song.info.format_output(config.SONGINFO_NOW_PLAYING))
                
            else:
                await ctx.send(embed=song.info.format_output(config.SONGINFO_QUEUE_ADDED))

        elif song.origin == linkutils.Origins.Playlist:
            embedvc = discord.Embed(
            colour= config.EMBED_COLOR_OK,
            description = config.SONGINFO_PLAYLIST_QUEUED
        )
            await ctx.send(embed=embedvc)

    @commands.command(name='loop', help=config.HELP_LOOP, aliases=['l'])
    async def _loop(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if await utils.play_check(ctx) == False:
            return

        if len(audiocontroller.playlist.playque) < 1 and current_guild.voice_client.is_playing() == False:
            embedvc = discord.Embed(
                colour= config.EMBED_COLOR_ERROR,
                description = "A fila está vazia :x:"
            )
            await ctx.send(embed=embedvc)
            return

        if audiocontroller.playlist.loop == False:
            audiocontroller.playlist.loop = True
            txt = "Loop ativado :arrows_counterclockwise:"
            
        else:
            audiocontroller.playlist.loop = False
            txt = "Loop desativado :x:"
            
        embedvc = discord.Embed(
            colour= config.EMBED_COLOR_OK,
            description = txt
            )
        await ctx.send(embed=embedvc)
            

    @commands.command(name='shuffle', help=config.HELP_SHUFFLE, aliases=['sh', 'a'])
    async def _shuffle(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            embedvc = discord.Embed(
            colour= config.EMBED_COLOR_ERROR,
            description = config.NO_GUILD_MESSAGE
            )
            await ctx.send(embed=embedvc)
            return
        
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            embedvc = discord.Embed(
                colour= config.EMBED_COLOR_ERROR,
                description = "A fila está vazia :x:"
            )
            await ctx.send(embed=embedvc)
            return

        audiocontroller.playlist.shuffle()
        embedvc = discord.Embed(
            colour= config.EMBED_COLOR_OK,
            description = "Fila aleatória :twisted_rightwards_arrows:"
        )
        await ctx.send(embed=embedvc)
    
        for song in list(audiocontroller.playlist.playque)[:config.MAX_SONG_PRELOAD]:
            asyncio.ensure_future(audiocontroller.preload(song))

    @commands.command(name='pause', help=config.HELP_PAUSE, aliases=['pausar'])
    async def _pause(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            embedvc = discord.Embed(
            colour= config.EMBED_COLOR_ERROR,
            description = config.NO_GUILD_MESSAGE
            )
            await ctx.send(embed=embedvc)
            return
        
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            return
        current_guild.voice_client.pause()
        embedvc = discord.Embed(
            colour= config.EMBED_COLOR_OK,
            description = "Música pausada :pause_button:"
        )
        await ctx.send(embed=embedvc)

    @commands.command(name='queue', help=config.HELP_QUEUE, aliases=['playlist', 'q'])
    async def _queue(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            embedvc = discord.Embed(
            colour= config.EMBED_COLOR_ERROR,
            description = config.NO_GUILD_MESSAGE
            )
            await ctx.send(embed=embedvc)
            return
        
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            await ctx.send("A fila está vazia :x:")
            return

        playlist = utils.guild_to_audiocontroller[current_guild].playlist

        # Embeds são limitados a 25 campos
        if config.MAX_SONG_PRELOAD > 25:
            config.MAX_SONG_PRELOAD = 25

        embed = discord.Embed(title=":scroll: Playlist [{}]".format(
            len(playlist.playque)), color=config.EMBED_COLOR, inline=False)

        for counter, song in enumerate(list(playlist.playque)[:config.MAX_SONG_PRELOAD], start=1):
            if song.info.title is None:
                embed.add_field(name="{}.".format(str(counter)), value="[{}]({})".format(
                    song.info.webpage_url, song.info.webpage_url), inline=False)
            else:
                embed.add_field(name="{}.".format(str(counter)), value="[{}]({})".format(
                    song.info.title, song.info.webpage_url), inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='stop', help=config.HELP_STOP, aliases=['st', 'parar'])
    async def _stop(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False
        if current_guild is None:
            embedvc = discord.Embed(
            colour= config.EMBED_COLOR_ERROR,
            description = config.NO_GUILD_MESSAGE
            )
            await ctx.send(embed=embedvc)
            return
        
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        embedvc = discord.Embed(
            colour= config.EMBED_COLOR_OK,
            description = "Todas as músicas canceladas :octagonal_sign:"
            )
        await ctx.send(embed=embedvc)

    @commands.command(name='skip', help=config.HELP_SKIP, aliases=['s', 'pular'])
    async def _skip(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False

        audiocontroller.timer.cancel()
        audiocontroller.timer = utils.Timer(audiocontroller.timeout_handler)

        if current_guild is None:
            embedvc = discord.Embed(
            colour= config.EMBED_COLOR_ERROR,
            description = config.NO_GUILD_MESSAGE
            )
            await ctx.send(embed=embedvc)
            return
        if current_guild.voice_client is None or (
                not current_guild.voice_client.is_paused() and not current_guild.voice_client.is_playing()):
            embedvc = discord.Embed(
            colour= config.EMBED_COLOR_ERROR,
            description = "A fila está vazia :x:"
            )
            await ctx.send(embed=embedvc)
            return
        current_guild.voice_client.stop()
        embedvc = discord.Embed(
            colour= config.EMBED_COLOR_OK,
            description = "Música pulada :fast_forward:"
            )
        await ctx.send(embed=embedvc)

    @commands.command(name='clear', help=config.HELP_CLEAR, aliases=['cl', 'limpar'])
    async def _clear(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.clear_queue()
        current_guild.voice_client.stop()
        audiocontroller.playlist.loop = False
        embedvc = discord.Embed(
            colour= config.EMBED_COLOR_OK,
            description = "Fila limpa :no_entry_sign:"
            )
        await ctx.send(embed=embedvc)

    @commands.command(name='prev', help=config.HELP_PREV, aliases=['back', 'voltar'])
    async def _prev(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False

        audiocontroller.timer.cancel()
        audiocontroller.timer = utils.Timer(audiocontroller.timeout_handler)

        if current_guild is None:
            embedvc = discord.Embed(
            colour= config.EMBED_COLOR_ERROR,
            description = config.NO_GUILD_MESSAGE
            )
            await ctx.send(embed=embedvc)
            return
        await utils.guild_to_audiocontroller[current_guild].prev_song()
        embedvc = discord.Embed(
            colour= config.EMBED_COLOR_OK,
            description = "Reproduzindo a música anterior :track_previous:"
            )
        await ctx.send(embed=embedvc)

    @commands.command(name='resume', help=config.HELP_RESUME)
    async def _resume(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            embedvc = discord.Embed(
            colour = config.EMBED_COLOR_OK,
            description = config.NO_GUILD_MESSAGE
            )
            await ctx.send(embed=embedvc)
            return
        
        current_guild.voice_client.resume()
        embedvc = discord.Embed(
            colour= config.EMBED_COLOR_ERROR,
            description = "Reproduzindo :arrow_forward:"
            )
        await ctx.send(embed=embedvc)

    @commands.command(name='songinfo', help=config.HELP_SONGINFO, aliases=["np"])
    async def _songinfo(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            embedvc = discord.Embed(
            colour= config.EMBED_COLOR_ERROR,
            description = config.NO_GUILD_MESSAGE
            )
            await ctx.send(embed=embedvc)
            return
        song = utils.guild_to_audiocontroller[current_guild].current_song
        if song is None:
            return
        await ctx.send(embed=song.info.format_output(config.SONGINFO_SONGINFO))

    @commands.command(name='history', help=config.HELP_HISTORY)
    async def _history(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx.message)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            embedvc = discord.Embed(
            colour= config.EMBED_COLOR_ERROR,
            description = config.NO_GUILD_MESSAGE
            )
            await ctx.send(embed=embedvc)
            return
        
        await ctx.send(embed=utils.guild_to_audiocontroller[current_guild].track_history())

    @commands.command(name='volume', help=config.HELP_VOL, aliases=["vol"])
    async def _volume(self, ctx, *args):
        if ctx.guild is None:
            embedvc = discord.Embed(
            colour= config.EMBED_COLOR_ERROR,
            description = config.NO_GUILD_MESSAGE
            )
            await ctx.send(embed=embedvc)
            return

        if await utils.play_check(ctx) == False:
            return

        if len(args) == 0:
            embedvc = discord.Embed(
            colour= config.EMBED_COLOR,
            description = "Volume atual: {}% :speaker:".format(utils.guild_to_audiocontroller[ctx.guild]._volume)
            )
            await ctx.send(embed=embedvc)
            return
        
        try:
            volume = args[0]
            volume = int(volume)
            if volume > 100 or volume < 0:
                raise Exception('')
            current_guild = utils.get_guild(self.bot, ctx.message)

            if utils.guild_to_audiocontroller[current_guild]._volume >= volume:
                txt = 'Volume alterado para {}% :sound:'.format(str(volume))
            else:
                txt = 'Volume alterado para {}% :loud_sound:'.format(str(volume))
            utils.guild_to_audiocontroller[current_guild].volume = volume
            embedvc = discord.Embed(
            colour= config.EMBED_COLOR_OK,
            description = txt
            )
            await ctx.send(embed=embedvc)
        except:
            embedvc = discord.Embed(
            colour= config.EMBED_COLOR_ERROR,
            description = "Erro: O volume precisa ser um número entre 1 e 100"
            )
            await ctx.send(embed=embedvc)

    @commands.command(name="lyrics", help=config.HELP_LYRICS)
    async def lyrics_command(self, ctx, name: t.Optional[str]):
        player = utils.get_guild(self.bot, ctx)
        song = utils.guild_to_audiocontroller[player].current_song
        name = song.info.title
        extract_lyrics = SongLyrics(config.API_KEY, config.GCS_ENGINE_ID)
        data = extract_lyrics.get_lyrics(name)
        
        async with ctx.typing():    
            if data == None:
                embedvc = discord.Embed(
                    colour= config.EMBED_COLOR_ERROR,
                    description = "Não foi possível encontrar essa letra!"
                    )
                return await ctx.send(embed=embedvc)
            
            if len(data["lyrics"]) > 3000:
                embedvc = discord.Embed(
                    colour= config.EMBED_COLOR_ERROR,
                    description = "A letra desta música é gigante. Desculpe, o discord não aceita mensagens tão grandes!"
                    )
                return await ctx.send(embed=embedvc)
            
            embed = discord.Embed(
                title=data['title'],
                description=data['lyrics'],
                colour=config.EMBED_COLOR,
                timestamp=dt.datetime.utcnow(),
            )
            await ctx.send(embed=embed)    
           
def setup(bot):
    bot.add_cog(Music(bot))
