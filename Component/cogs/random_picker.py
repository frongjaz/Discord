import random
import asyncio
from discord.ext import commands

# รายชื่อผู้เล่น
participants = [
    "Moo Deng Za Mak",
    "Aeolus_Kevin",
    "สุดหล่อ(BEER)",
    "OliverxX",
    "SD TARANTAMAD • assasin",
    "FPXD.",
    "SD | ReaLBesT",
    "88888888 (เอก)",
    "SD | Stinger • Impaler",
    "SD | NAPAT1KOL",
    "แข็งโป๊ก (เก้า)",
    "HUMTaYanFaaa (NU)",
    "SD TARANTAMAD • assasin",
    "aa17",
    "ballchang (คำแพม)",
    "ถอกยันโคน แพท",
    "นุ่มนิ่ม",
    "SD | waller/โต้ง",
    "REGENCY",
    "Bumble",
    "Stal2Du5T",
]

class RandomPicker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="random", help="สุ่มชื่อจากรายการ")
    async def random_pick(self, ctx):
        await ctx.send("🎰 กำลังสุ่มรายชื่อ...")

        # แอนิเมชันการสุ่ม
        shuffled_names = participants.copy()
        random.shuffle(shuffled_names)
        animation_text = ""
        for i in range(10):  # แสดงรายชื่อแบบสุ่ม 10 ครั้ง
            selected = random.choice(shuffled_names)
            animation_text = f"🎲 กำลังสุ่ม: **{selected}**"
            await ctx.edit_last_message(content=animation_text)
            await asyncio.sleep(0.5)

        # ผลลัพธ์สุดท้าย
        winner = random.choice(participants)
        result_text = f"🎉 ชื่อที่สุ่มได้คือ: **{winner}** 🎊"
        await ctx.edit_last_message(content=result_text)

def setup(bot):
    bot.add_cog(RandomPicker(bot))
