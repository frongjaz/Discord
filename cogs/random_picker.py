import random
import asyncio
from discord.ext import commands

class RandomPicker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def random(self, ctx):
        msg = await ctx.send("🎰 กำลังสุ่มรายชื่อ...")

        names = [
            "Moo Deng Za Mak", "Aeolus_Kevin", "สุดหล่อ(BEER)", "OliverxX",
            "SD TARANTAMAD • assasin", "FPXD.", "SD | ReaLBesT", "88888888 (เอก)",
            "SD | Stinger • Impaler", "SD | NAPAT1KOL", "แข็งโป๊ก (เก้า)",
            "HUMTaYanFaaa (NU)", "SD TARANTAMAD • assasin", "aa17 —",
            "ballchang (คำแพม)", "ถอกยันโคน แพท", "นุ่มนิ่ม", "SD | waller/โต้ง",
            "REGENCY", "Bumble", "Stal2Du5T"
        ]

        for _ in range(5):  # สุ่มชื่อ 5 ครั้ง
            await msg.edit(content="🔄 กำลังสุ่มชื่อ...")
            await asyncio.sleep(0.5)  # รอ 0.5 วินาที

        chosen_name = random.choice(names)
        await msg.edit(content=f"🎰 ชื่อที่สุ่มได้: {chosen_name}")

def setup(bot):
    bot.add_cog(RandomPicker(bot))
