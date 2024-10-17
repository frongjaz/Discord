import os
import random
import discord
import requests
from discord.ext import commands
from threading import Thread
from myserver import server_on  # Assuming this starts your server
from Component import new_member
from Component import noti_c3  
from Component import rank  
from Component import sheet

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

target_channel_id = 1290924217184948236
GR_channel_id = 1242868461982580807
SweetDessert_role = 1218124815378940035

# เมื่อบอทพร้อมทำงาน
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")
    
    # เริ่มการแจ้งเตือนทุกวันศุกร์
    noti_c3.friday_reminder.start(bot)
    noti_c3.saturday_reminder.start(bot)
# เรียกใช้งานฟังก์ชัน on_member_join จาก new_member.py
@bot.event
async def on_member_join(member):
    await new_member.on_member_join(bot, member)

# เมื่อมีข้อความส่งมา
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == GR_channel_id and message.content.isdigit():
        number = int(message.content)
        username = message.author.display_name

        # ข้อมูลที่ต้องการส่งไปยัง Google Sheets
        data = {
            'name': username,
            'GR_value': number
        }

        # URL ของ Web App ที่ได้จาก Google Apps Script
        url = 'https://script.google.com/macros/s/AKfycbxdlxls3pHHab_b_fGVdBjGUNsczUGiOKrdd3STi-BFudmRZHLrfaARResrkuUPs_Tn1w/exec'

        # ส่งข้อมูลไปยัง Google Sheets
        response = requests.post(url, json=data)

        if response.status_code == 200:
            await message.channel.send(f"ข้อมูลของคุณ {username} ได้ถูกบันทึกแล้ว: {number}")
        else:
            await message.channel.send("เกิดข้อผิดพลาดในการบันทึกข้อมูล กรุณาแจ้งบอสฟร้อง.")

    if message.channel.id == target_channel_id and message.content.isdigit():
        number = int(message.content)
        username = message.author.display_name
        
        # ใช้ฟังก์ชัน add_user เพื่อเพิ่มหรืออัปเดตข้อมูลผู้ใช้
        old_number, user_exists = rank.add_user(username, number)

        # คำนวณการเปลี่ยนแปลงและเปอร์เซ็นต์
        if user_exists:
            difference = number - old_number
            if old_number != 0:
                percentage_change = (difference / old_number) * 100
            else:
                percentage_change = 0

            # แสดงข้อความการเปลี่ยนแปลง
            change_direction = "เพิ่มขึ้น" if difference > 0 else "ลดลง" if difference < 0 else "ไม่เปลี่ยนแปลง"
            await message.channel.send(
                f"คุณ {username} ได้เปลี่ยนตราใหญ่ (HSOA) จาก {old_number} เป็น {number} "
                f"({change_direction} {abs(difference)} หน่วย, {abs(percentage_change):.2f}%)"
            )
        else:
            await message.channel.send(f"คุณ {username} มีตราใหญ่ (HSOA) : {number}")

    # แสดงอันดับ HSOA
    if message.content.lower() == '!rank':
        ranking_message = rank.rank_numbers()
        await message.channel.send(ranking_message)

    # Reset ข้อมูล
    if message.content.lower() == '!clear':
        rank.user_numbers = []
        await message.channel.send("Clear เรียบร้อย!")

@bot.tree.command(name='rank', description='แสดง rank ของคนมี HSOA')
async def rankcommand(interaction):
    await interaction.response.send_message(rank.rank_numbers())

# Start the bot and the server concurrently
if __name__ == "__main__":
    flask_thread = Thread(target=server_on)
    flask_thread.start()
    bot.run(os.getenv('TOKEN'))
