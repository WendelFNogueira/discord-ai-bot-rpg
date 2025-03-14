import discord
from discord.ext import commands
import yt_dlp

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self.song_queue = []

    @commands.command(name="play", help="Toca uma música a partir de uma URL do YouTube. Exemplo: /play <URL>")
    async def play(self, ctx, url: str):
        voice_channel = ctx.author.voice.channel
        if not voice_channel:
            await ctx.send("Você precisa estar em um canal de voz!")
            return

        if not self.voice_client:
            self.voice_client = await voice_channel.connect()

        ydl_opts = {"format": "bestaudio/best", "postprocessors": [{"key": "FFmpegExtractAudio"}]}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                for entry in info['entries']:
                    self.song_queue.append(entry)
            else:
                self.song_queue.append(info)

        if not self.voice_client.is_playing():
            await self.play_next_song(ctx)

    async def play_next_song(self, ctx):
        if self.song_queue:
            song = self.song_queue.pop(0)
            url2 = song["url"]
            self.voice_client.play(discord.FFmpegPCMAudio(url2), after=lambda e: self.bot.loop.create_task(self.play_next_song(ctx)))
            await ctx.send(f"🎵 Tocando: {song['title']}")
        else:
            await ctx.send("A fila de músicas está vazia!")

    @commands.command(name="skip", help="Pula a música atual.")
    async def skip(self, ctx):
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()
            await ctx.send("⏭️ Música pulada!")

    @commands.command(name="stop", help="Para a música e desconecta o bot do canal de voz.")
    async def stop(self, ctx):
        if self.voice_client:
            self.song_queue.clear()
            await self.voice_client.disconnect()
            self.voice_client = None
            await ctx.send("⏹️ Música parada!")

async def setup(bot):
    await bot.add_cog(Music(bot))