import discord
from datetime import datetime, timedelta
import asyncio
import pytz

TZ_THAILAND = pytz.timezone('Asia/Bangkok')
SweetDessert_role = 1218124815378940035
mention_role = f"<@&{SweetDessert_role}>"

class Miniboss:
    def __init__(self, bot, name, spawn_time_range, color, image_url=None):
        self.bot = bot
        self.name = name
        self.spawn_time_range = spawn_time_range  
        self.color = color  
        self.image = image_url  
        self.instances = []  

    def add_death_time(self, death_time_str):
        """เพิ่มเวลาตายให้กับบอส และสร้าง instance ใหม่ใน instances"""
        try:
            now = datetime.now(TZ_THAILAND)
            death_time = datetime.strptime(death_time_str, '%H:%M').replace(
                year=now.year, month=now.month, day=now.day)
            death_time = TZ_THAILAND.localize(death_time)
            self.instances.append(death_time)  # เพิ่มเวลาตายใหม่เข้าไปใน instances
            return True
        except ValueError:
            return False

    def calculate_spawn_time(self, death_time):
        """คำนวณเวลาที่บอสจะเกิดใหม่ โดยอิงจากเวลาตายที่ให้มา"""
        min_spawn_time = death_time + timedelta(hours=self.spawn_time_range[0])
        max_spawn_time = death_time + timedelta(hours=self.spawn_time_range[1])
        return (min_spawn_time, max_spawn_time)

    async def check_spawn_time(self, channel):
        """ตรวจสอบและประกาศเวลาที่บอสจะเกิดใหม่สำหรับทุก instance ที่มีอยู่"""
        while True:
            await asyncio.sleep(60)  # เช็คทุกๆ 60 วินาที
            current_time = datetime.now(TZ_THAILAND)

            for death_time, location in self.instances[:]:  # ใช้ copy ของ list เพื่อวนลูปได้อย่างปลอดภัย
                spawn_time = self.calculate_spawn_time(death_time)

                if spawn_time[0] <= current_time <= spawn_time[1]:
                    spawn_location_description = self.get_spawn_location()
                    await channel.send(f"{mention_role} บอส {self.name} เกิดแล้ว {location}!") 
                    embed = discord.Embed(
                        title=f" บอส {self.name} เกิดแล้ว {location}! 🎉",
                        description=(f"บอส {self.name} ได้เกิดใหม่ที่ {spawn_location_description} {location}. \n"
                                    f"⏳ บอสจะเกิดในช่วงเวลา **{spawn_time[0].strftime('%H:%M')} - {spawn_time[1].strftime('%H:%M')}**."),
                        color=discord.Color.from_str(self.color)
                    )
                    if self.image:
                        embed.set_image(url=self.image)
                    await channel.send(embed=embed)

                    self.instances.remove((death_time, location))

    def get_spawn_location(self):
        """แสดงสถานที่เกิดบอสตามสี"""
        if self.color == "#000000":
            return "วงสีดำ"
        elif self.color == "#FF0000":
            return "วงสีแดง"
        elif self.color == "#0000FF":
            return "วงสีฟ้า"
        elif self.color == "#00FF00":
            return "วงสีเขียว"
        else:
            return "วงสีอื่น"

    async def spawn(self, input_str, channel):
        """เพิ่มเวลาตายใหม่ และเริ่มเช็คเวลาที่บอสจะเกิด"""
        input_parts = input_str.split()  # แยกข้อความที่กรอกมา
        death_time_str = input_parts[0]  # แยกเวลาตายจาก input
        location = ' '.join(input_parts[1:]) if len(input_parts) > 1 else ""  # ถ้ามีข้อมูลเพิ่มเติมให้ใช้เป็นสถานที่

        # ตรวจสอบเวลาตาย
        if self.add_death_time(death_time_str):
            if len(self.instances) > 0 and isinstance(self.instances[-1], tuple):
                self.instances[-1] = (self.instances[-1][0], location)  # อัพเดตสถานที่ใน instance ล่าสุด
            else:
                self.instances.append((self.death_time, location))  # เพิ่ม instance ใหม่ถ้าไม่มี

            death_time, _ = self.instances[-1]  # เวลาตายล่าสุด
            spawn_times = self.calculate_spawn_time(death_time)
            spawn_location_description = self.get_spawn_location()

            embed = discord.Embed(
                title=f"🦹‍♂️ บอส {self.name} ตายแล้ว",
                description=(
                    f"🕒 บอส {self.name} ตายเมื่อเวลา **{death_time_str}**.\n"
                    f"⏳ บอสจะเกิดในช่วงเวลา **{spawn_times[0].strftime('%H:%M')} - {spawn_times[1].strftime('%H:%M')}**.\n"
                    f"โดยเกิดที่ {spawn_location_description} {location}"
                ),
                color=discord.Color.from_str(self.color)
            )
            if self.image:
                embed.set_image(url=self.image)
            await channel.send(embed=embed)

            # เริ่มเช็คเวลาที่บอสจะเกิด
            await self.check_spawn_time(channel)
        else:
            await channel.send("รูปแบบเวลาไม่ถูกต้อง กรุณาใช้รูปแบบ HH:MM")
