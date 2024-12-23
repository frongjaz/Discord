import random
import asyncio
from discord.ext import commands

class RandomPicker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def random(self, ctx):
        # ข้อความเริ่มต้น
        msg = await ctx.send("🎰 กำลังสุ่มรายชื่อ...")

        # รายชื่อที่สุ่ม
        names = [
            "Moo Deng Za Mak", "Aeolus_Kevin", "สุดหล่อ(BEER)", "OliverxX",
            "SD TARANTAMAD • assasin", "FPXD.", "SD | ReaLBesT", "88888888 (เอก)",
            "SD | Stinger • Impaler", "SD | NAPAT1KOL", "แข็งโป๊ก (เก้า)",
            "HUMTaYanFaaa (NU)", "SD TARANTAMAD • assasin", "aa17 —",
            "ballchang (คำแพม)", "ถอกยันโคน แพท", "นุ่มนิ่ม", "SD | waller/โต้ง",
            "REGENCY", "Bumble", "Stal2Du5T"
        ]

        # สุ่มชื่อทุกๆ 0.5 วินาที
        for _ in range(5):  # เปลี่ยนข้อความ 5 ครั้ง
            await msg.edit(content=f"🎰 กำลังสุ่ม: {random.choice(names)}")
            await asyncio.sleep(0.5)  # รอ 0.5 วินาที

        # ผลลัพธ์การสุ่ม
        chosen_name = random.choice(names)
        await msg.edit(content=f"🎰 ชื่อที่สุ่มได้: {chosen_name}")

# ฟังก์ชัน setup ไม่ต้องใช้ await ที่นี่
def setup(bot):
    bot.add_cog(RandomPicker(bot))  # ไม่ต้อง await
