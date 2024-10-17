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
from Component import miniboss

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

target_channel_id = 1290924217184948236
GR_channel_id = 1242868461982580807
SweetDessert_role = 1218124815378940035
url = 'https://script.google.com/macros/s/AKfycbxdlxls3pHHab_b_fGVdBjGUNsczUGiOKrdd3STi-BFudmRZHLrfaARResrkuUPs_Tn1w/exec'

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

@bot.event
async def on_member_join(member):
    await new_member.on_member_join(bot, member)


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == GR_channel_id and message.content.isdigit():
        number = int(message.content.replace(',', ''))  # ลบคอมม่า
        username = message.author.display_name
        # ดึงค่าที่เก่าจาก Google Sheets
        previous_value = get_previous_value(username)

        # ส่งข้อมูลไปยัง Google Sheets
        response = requests.post(url, json={'name': username, 'GR_value': number})

        if response.status_code == 200:

            if previous_value is not None:
                difference = number - previous_value
                if previous_value != 0:
                    percentage_change = (difference / previous_value) * 100
                else:
                    percentage_change = 0

                if difference > 0:
                    change_direction = "เพิ่มขึ้น"
                    emoji = "📈"
                    color = discord.Color.green()
                    sign = "+"         
                elif difference < 0:
                    change_direction = "ลดลง"
                    emoji = "📉"
                    color = discord.Color.red()
                    sign = "-"
                else:
                    change_direction = "ไม่เปลี่ยนแปลง"
                    emoji = "🔄"
                    color = discord.Color.gold()
                    sign = ""
                embed = discord.Embed(
                    title=f"บันทึกข้อมูลสำเร็จ!",
                    description=f"ข้อมูลของคุณ **{username}** ได้ถูกบันทึกแล้ว: **{number}**",
                    color=color
                )
                embed.add_field(
                    name=f"การเปลี่ยนแปลง: **{change_direction}** {emoji}",
                    value=f"**{abs(difference)} หน่วย** ({sign}{abs(percentage_change):.2f}%)",
                    inline=False
                )

                # เพิ่มฟิลด์เพิ่มเติมเพื่อให้ข้อความดูดีขึ้น
                embed.add_field(
                    name="📅 วันที่:",
                    value=f"**{discord.utils.format_dt(discord.utils.utcnow(), 'D')}**",  # แสดงวันที่ปัจจุบัน
                    inline=True
                )

                embed.add_field(
                    name="⌛ เวลา:",
                    value=f"**{discord.utils.format_dt(discord.utils.utcnow(), 'T')}**",  # แสดงเวลาปัจจุบัน
                    inline=True
                )
                embed.set_footer(text="SweetDessert GR | ขอบคุณที่ใช้งาน!", icon_url="https://i.imgur.com/ZdfJpK4.png")
                await message.channel.send(embed=embed)
        else:
            await message.channel.send("เกิดข้อผิดพลาดในการบันทึกข้อมูล กรุณาแจ้งบอสฟร้อง.")

    if message.channel.id == target_channel_id and message.content.isdigit():
        number = int(message.content)
        username = message.author.display_name
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
def get_previous_value(username):
    # ฟังก์ชันนี้จะต้องไปดึงค่าจาก Google Sheets เพื่อหาค่าที่เก่าก่อนหน้านี้
    response = requests.get(url + '?username=' + username)
    if response.status_code == 200:
        data = response.json()
        return data.get('GR_value')  # ค่าที่เก่าจะต้องอยู่ในฟิลด์นี้
    return None

@bot.command(name='miniboss')
async def create_miniboss(ctx, boss_name: str, death_time: str):
    for boss in miniboss.minibosses:
        if boss.name == boss_name:
            await boss.spawn(death_time, ctx)
            return
    
    await ctx.send("ไม่พบชื่อบอสที่กรอก กรุณาลองใหม่อีกครั้ง.")

@bot.tree.command(name='rank', description='แสดง rank ของคนมี HSOA')
async def rankcommand(interaction):
    await interaction.response.send_message(rank.rank_numbers())

@bot.tree.command(name='boss_info', description='แสดงข้อมูลบอสที่เลือก')
async def boss_info(interaction: discord.Interaction, boss_name: str):
    # ค้นหาบอสในรายชื่อ minibosses
    miniboss = next((b for b in miniboss.minibosses if b.name == boss_name), None)
    
    if miniboss:
        # สร้าง Embed สำหรับแสดงข้อมูล
        embed = discord.Embed(
            title=f"ข้อมูลบอส: {miniboss.name}",
            description=f"บอสจะเกิดใน {miniboss.spawn_time[0]} - {miniboss.spawn_time[1]} ชั่วโมงหลังจากตาย",
            color=discord.Color.blue()
        )
        embed.set_image(url=miniboss.image)  # แนบภาพบอส
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("ไม่พบข้อมูลบอสที่เลือก.")

# Start the bot and the server concurrently
if __name__ == "__main__":
    flask_thread = Thread(target=server_on)
    flask_thread.start()
    bot.run(os.getenv('TOKEN'))
