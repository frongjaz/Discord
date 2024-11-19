import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
import os

# ตั้งค่า Youtube_DL สำหรับดึงข้อมูลลิงก์และเสียง
youtube_dl.utils.bug_reports_message = lambda: ""
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        
        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join', help='ให้บอทเข้าร่วมห้องเสียง')
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("คุณต้องอยู่ในห้องเสียงเพื่อให้บอทร่วม")

    @commands.command(name="play")
    async def play(self, ctx, *, url):
        try:
            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print(f'Error: {e}') if e else None)
            await ctx.send(f'🎶 กำลังเล่น: {player.title}')
        except Exception as e:
            await ctx.send(f"❌ ไม่สามารถเล่นเพลงได้: {str(e)}")

    @commands.command(name='pause', help='หยุดเพลงชั่วคราว')
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ หยุดเพลงชั่วคราว")
        else:
            await ctx.send("❌ ไม่มีเพลงที่กำลังเล่นอยู่")

    @commands.command(name='resume', help='เล่นเพลงต่อ')
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ เล่นเพลงต่อ")
        else:
            await ctx.send("❌ ไม่มีเพลงที่ถูกหยุดชั่วคราว")

    @commands.command(name='stop', help='หยุดเพลง')
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("⏹️ หยุดเพลงและออกจากห้องเสียง")

    @commands.command(name='leave', help='ให้บอทออกจากห้องเสียง')
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("👋 ออกจากห้องเสียงแล้ว")

def setup(bot):
    bot.add_cog(Music(bot))
