import discord
import asyncio
import random

class MiniBoss:
    def __init__(self, name, respawn_time, color, image):
        self.name = name
        self.respawn_time = respawn_time  # (min_time, max_time)
        self.color = color
        self.image = image

    async def announce_death(self, ctx, death_time):
        await ctx.send(f"บอส **{self.name}** ตายเมื่อเวลา {death_time}!")
        
        # คำนวณเวลาที่บอสจะเกิดใหม่
        respawn_duration = random.uniform(self.respawn_time[0] * 3600, self.respawn_time[1] * 3600)
        await asyncio.sleep(respawn_duration)

        # เมื่อบอสเกิดใหม่
        await ctx.send(f"บอส **{self.name}** เกิดแล้ว! ", file=discord.File(self.image))

# สร้างรายชื่อบอส
minibosses = [
    MiniBoss("อังโกลท์", (3.5, 6.5), "วงดำ", 'miniboos1.jpg'),
    MiniBoss("คิอารอน", (4.5, 7.5), "วงแดง", 'miniboos1.jpg'),
    MiniBoss("กริซ", (5.5, 8.5), "วงฟ้า", 'miniboos1.jpg'),
    MiniBoss("อินเฟรโน", (6.5, 9.5), "วงเขียว", 'miniboos1.jpg'),
]

async def create_miniboss(ctx, name, death_time):
    miniboss = next((mb for mb in minibosses if mb.name == name), None)
    if miniboss:
        await miniboss.announce_death(ctx, death_time)
    else:
        await ctx.send("ไม่พบบอสที่ระบุ.")
