import discord
from datetime import datetime, timedelta
import random
import asyncio
import pytz 

TZ_THAILAND = pytz.timezone('Asia/Bangkok')

class Miniboss:
    def __init__(self, bot, name, spawn_time_range, color, image_url=None):
        self.bot = bot  # เพิ่ม bot ที่ส่งเข้ามา
        self.name = name  # ชื่อบอส
        self.spawn_time_range = spawn_time_range  # ช่วงเวลาที่บอสจะเกิดใหม่ เช่น (3.5, 6.5) ชั่วโมง
        self.color = color  # สีของวง (เพื่อการอ้างอิง)
        self.image = image_url  # URL รูปภาพของบอส
        self.death_time = None  # เวลาที่บอสตาย

    def set_death_time(self, death_time_str):
        """ตั้งเวลาเมื่อตาย โดยรับค่าเวลาตายในรูปแบบ string 'HH:MM'"""
        try:
            now = datetime.now(TZ_THAILAND)  
            death_time = datetime.strptime(death_time_str, '%H:%M').replace(
                year=now.year, month=now.month, day=now.day)
            death_time = TZ_THAILAND.localize(death_time)  
            self.death_time = death_time
            return True
        except ValueError:
            return False

    def calculate_spawn_time(self):
        """คำนวณเวลาที่บอสจะเกิดใหม่ โดยอิงจากช่วงเวลาที่กำหนด"""
        if self.death_time:
            min_spawn_time = self.death_time + timedelta(hours=self.spawn_time_range[0])
            max_spawn_time = self.death_time + timedelta(hours=self.spawn_time_range[1])
            return (min_spawn_time, max_spawn_time)
        return None

    async def check_spawn_time(self, channel):
        """ตรวจสอบเวลาที่บอสจะเกิด"""
        while True:
            await asyncio.sleep(60) 
            current_time = datetime.now(TZ_THAILAND) 
            spawn_time = self.calculate_spawn_time()
            
            if spawn_time and spawn_time[0] <= current_time <= spawn_time[1]:
                embed = discord.Embed(
                    title=f"🎉 บอส {self.name} เกิดแล้ว! 🎉",
                    description=f"บอส {self.name} ได้เกิดใหม่ในขณะนี้ที่ {current_time.strftime('%H:%M')}",
                    color=discord.Color.from_str(self.color)
                )
                if self.image:
                    embed.set_image(url=self.image)
                await channel.send(embed=embed)
                break



    async def spawn(self, death_time_str, channel):
        """เรียกใช้เมื่อบอสตาย และแจ้งให้ผู้ใช้ทราบ"""
        if self.set_death_time(death_time_str):
            spawn_times = self.calculate_spawn_time()
            # เปลี่ยนให้จุดเกิดแสดงเป็นข้อความแทนการใช้รหัสสี
            spawn_location_description = ""
            if self.color == "#000000":
                spawn_location_description = "วงสีดำ"
            elif self.color == "#FF0000":
                spawn_location_description = "วงสีแดง"
            elif self.color == "#0000FF":
                spawn_location_description = "วงสีฟ้า"
            elif self.color == "#00FF00":
                spawn_location_description = "วงสีเขียว"
            else:
                spawn_location_description = "จุดเกิดไม่ทราบ"

            embed = discord.Embed(
                title=f"🦹‍♂️ บอส {self.name} ตายแล้ว",
                description=(
                    f"🕒 บอส {self.name} ตายเมื่อเวลา **{death_time_str}**.\n"
                    f"⏳ บอสจะเกิดในช่วงเวลา **{spawn_times[0].strftime('%H:%M')} - {spawn_times[1].strftime('%H:%M')}**.\n"
                    f"{spawn_location_description}"
                ),
                color=discord.Color.from_str(self.color)  
            )
            if self.image:
                embed.set_image(url=self.image)
            await channel.send(embed=embed)
            
            # เริ่มเช็คเวลาเกิดบอสในช่องที่กำหนด
            await self.check_spawn_time(channel)

        else:
            await channel.send("รูปแบบเวลาไม่ถูกต้อง กรุณาใช้รูปแบบ HH:MM")


