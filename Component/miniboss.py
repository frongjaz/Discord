import discord
from datetime import datetime, timedelta
import pytz
import asyncio

SweetDessert_role = 1218124815378940035
mention_role = f"<@&{SweetDessert_role}>"
TZ_THAILAND = pytz.timezone('Asia/Bangkok')

class Miniboss:
    def __init__(self, bot, name, spawn_time_range, color, image_url=None):
        self.bot = bot
        self.name = name
        self.spawn_time_range = spawn_time_range
        self.color = color
        self.image = image_url
        self.instances = []  # สร้าง list เพื่อเก็บ instances ของ death_time และ location

    def add_death_time(self, death_time_str):
        """เพิ่มเวลาตาย"""
        try:
            now = datetime.now(TZ_THAILAND)
            death_time = datetime.strptime(death_time_str, '%H:%M').replace(
                year=now.year, month=now.month, day=now.day)
            death_time = TZ_THAILAND.localize(death_time)
            self.death_time = death_time  # ตั้งค่า death_time
            return True
        except ValueError:
            return False

    def calculate_spawn_time(self, death_time):
        """คำนวณเวลาที่บอสจะเกิดใหม่ โดยอิงจากช่วงเวลาที่กำหนด"""
        min_spawn_time = death_time + timedelta(hours=self.spawn_time_range[0])
        max_spawn_time = death_time + timedelta(hours=self.spawn_time_range[1])
        return (min_spawn_time, max_spawn_time)

    def get_spawn_location(self):
        """แสดงจุดเกิดตามสี"""
        if self.color == "#000000":
            return "ที่วงสีดำ"
        elif self.color == "#FF0000":
            return "ที่วงสีแดง"
        elif self.color == "#0000FF":
            return "ที่วงสีฟ้า"
        elif self.color == "#00FF00":
            return "ที่วงสีเขียว"
        else:
            return "ที่วงสีอื่น"

    async def check_spawn_time(self, channel):
        """ตรวจสอบเวลาที่บอสจะเกิด"""
        while True:
            await asyncio.sleep(60)
            current_time = datetime.now(TZ_THAILAND)

            for death_time, location in self.instances[:]:  # ใช้ copy ของ list เพื่อวนลูปได้อย่างปลอดภัย
                spawn_time = self.calculate_spawn_time(death_time)

                if spawn_time[0] <= current_time <= spawn_time[1]:
                    spawn_location_description = self.get_spawn_location()
                    await channel.send(f"{mention_role} บอส {self.name} เกิดแล้ว {spawn_location_description} {location}!") 
                    embed = discord.Embed(
                        title=f"บอส {self.name} เกิดแล้ว {location}! 🎉",
                        description=(f"บอส {self.name} ได้เกิดใหม่ที่ {spawn_location_description} {location}.\n"
                                     f"⏳ บอสจะเกิดในช่วงเวลา **{spawn_time[0].strftime('%H:%M')} - {spawn_time[1].strftime('%H:%M')}**."),
                        color=discord.Color.from_str(self.color)
                    )
                    if self.image:
                        embed.set_image(url=self.image)
                    await channel.send(embed=embed)

                    self.instances.remove((death_time, location))  # ลบ instance ที่บอสเกิดแล้วออก

    async def spawn(self, input_str, channel):
        """เพิ่มเวลาตายใหม่ และเริ่มเช็คเวลาที่บอสจะเกิด"""
        print(f"Input String: '{input_str}'")  # ตรวจสอบค่าที่ส่งเข้าไป
        input_parts = input_str.split()  # แยกข้อความที่กรอกมา
        print(f"Input Parts: {input_parts}")  # ตรวจสอบค่าที่แยกได้
        death_time_str = input_parts[0]
        location = ' '.join(input_parts[1:]) if len(input_parts) > 1 else ""  # ดึงค่าตำแหน่งจาก input

        if self.add_death_time(death_time_str):
            # เพิ่มข้อมูลเข้าไปใน instances เป็น tuple
            self.instances.append((self.death_time, location))  # เพิ่ม instance ใหม่
            death_time, _ = self.instances[-1]  # เวลาตายล่าสุด
            spawn_times = self.calculate_spawn_time(death_time)
            spawn_location_description = self.get_spawn_location()

            # สร้าง embed
            embed = discord.Embed(
                title=f"🦹‍♂️ บอส {self.name} ตายแล้ว {location}",  # เพิ่ม location ใน title
                description=( 
                    f"🕒 บอส {self.name} ตายเมื่อเวลา **{death_time_str}**.\n"
                    f"⏳ บอสจะเกิดในช่วงเวลา **{spawn_times[0].strftime('%H:%M')} - {spawn_times[1].strftime('%H:%M')}**.\n"
                    f"โดยเกิดที่ {spawn_location_description} {location}"  # เพิ่ม location ใน description
                ),
                color=discord.Color.from_str(self.color)
            )
            if self.image:
                embed.set_image(url=self.image)
            await channel.send(embed=embed)

            await self.check_spawn_time(channel)
        else:
            await channel.send("รูปแบบเวลาไม่ถูกต้อง กรุณาใช้รูปแบบ HH:MM")
