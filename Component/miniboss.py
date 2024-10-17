import discord
from datetime import datetime, timedelta
import random

class Miniboss:
    def __init__(self, name, spawn_time_range, color, image_url=None):
        self.name = name  # ชื่อบอส
        self.spawn_time_range = spawn_time_range  # ช่วงเวลาที่บอสจะเกิดใหม่ เช่น (3.5, 6.5) ชั่วโมง
        self.color = color  # สีของวง (เพื่อการอ้างอิง)
        self.image = image_url  # URL รูปภาพของบอส
        self.death_time = None  # เวลาที่บอสตาย

    def set_death_time(self, death_time_str):
        """ตั้งเวลาเมื่อตาย โดยรับค่าเวลาตายในรูปแบบ string 'HH:MM'"""
        try:
            now = datetime.now()
            death_time = datetime.strptime(death_time_str, '%H:%M').replace(
                year=now.year, month=now.month, day=now.day)
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
        else:
            await channel.send("รูปแบบเวลาไม่ถูกต้อง กรุณาใช้รูปแบบ HH:MM")

url = "https://scontent.fbkk29-4.fna.fbcdn.net/v/t39.30808-6/463103563_122106380414560606_7643064554048604016_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=aa7b47&_nc_ohc=k4plQ7Ge2JYQ7kNvgE2RCRr&_nc_zt=23&_nc_ht=scontent.fbkk29-4.fna&_nc_gid=AkaTEo2eD5El_nEMeaWcc4e&oh=00_AYC7KNk25yQO0Gf02tQRapY6I3WFDoOixryPxwMuhC8ZCg&oe=67168F99"
# รายการบอสขนาดเล็ก
minibosses = [
    Miniboss("อังโกลท์", (3.5, 6.5), "#000000", url),  # วงดำ
    Miniboss("คิอารอน", (4.5, 7.5), "#FF0000", url),  # วงแดง
    Miniboss("กริซ", (5.5, 8.5), "#0000FF", url),  # วงฟ้า
    Miniboss("อินเฟรโน", (6.5, 9.5), "#00FF00", url),  # วงเขียว
]
