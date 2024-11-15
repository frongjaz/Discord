import discord
from discord.ext import commands
import youtube_dl
import asyncio
import yt_dlp as youtube_dl

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
ffmpeg_options = {'options': '-vn'}
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

# Music Cog class
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join', help='ให้บอทเข้าร่วมห้องเสียง')
    async def join(self, ctx):
        if ctx.author.voice:
            # ตรวจสอบว่าบอทเชื่อมต่ออยู่ใน channel หรือไม่
            if ctx.voice_client is not None:
                return await ctx.send("บอทเชื่อมต่อกับห้องเสียงอยู่แล้ว")
            
            # ถ้ายังไม่ได้เชื่อมต่อ, ให้บอทเชื่อมต่อ
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f"บอทเข้าร่วมช่อง {channel.name} แล้ว")
        else:
            await ctx.send("คุณต้องอยู่ในห้องเสียงเพื่อให้บอทร่วม")


    @commands.command(name='play', help='เล่นเพลงจาก YouTube')
    async def play(self, ctx, *, url):
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Error: {e}') if e else None)
        await ctx.send(f'🎶 กำลังเล่น: {player.title}')

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
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("⏹️ หยุดเพลงและออกจากห้องเสียง")
        else:
            await ctx.send("❌ บอทยังไม่ได้อยู่ในห้องเสียง")
