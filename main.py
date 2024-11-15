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
icon = "https://i.imgur.com/ZdfJpK4.png"
target_channel_id = 1290924217184948236
GR_channel_id = 1242868461982580807
SweetDessert_role = 1218124815378940035
url = 'https://script.google.com/macros/s/AKfycbyA1NsScYpN6MpdKVn8FXHdnwiK2jPnk34WzDsvzm-OtcD5oXO9rUuj4rMoRSaMRSqzGw/exec'

minibosses = [
    miniboss.Miniboss(bot, "อังโกลท์", (3.5, 6.5), "#000000", "https://img2.pic.in.th/pic/baf275d47676440180d1717c8c2198c4.png"),
    miniboss.Miniboss(bot, "คิอารอน", (4.5, 7.5), "#FF0000", "https://img2.pic.in.th/pic/f5af6ac6a95ac458c9ce84009e113e40.png"),
    miniboss.Miniboss(bot, "กริซ", (5.5, 8.5), "#0000FF", "https://img5.pic.in.th/file/secure-sv1/fedd60ce9d12fa6e087066cb11d08615.png"),
    miniboss.Miniboss(bot, "อินเฟรโน", (6.5, 9.5), "#00FF00", "https://img5.pic.in.th/file/secure-sv1/50b2d485c60420674a6962f1da60311a.png"),
    miniboss.Miniboss(bot,"รีอันเต",(5.5,8.5),"#00FF00","https://img2.pic.in.th/pic/19ef590c49fd82d7bd82628b79068065.png"),
    miniboss.Miniboss(bot,"เซรอน",(6.5,9.5),"#0000FF","https://img5.pic.in.th/file/secure-sv1/dbb09775942d744201c9a53e3829f66a.png"),
    miniboss.Miniboss(bot,"โกสต์มอล",(7.5,10.5),"#FF0000","https://img5.pic.in.th/file/secure-sv1/cff5951bcbb5235e295f07bc6eea77f6.png"),
    miniboss.Miniboss(bot,"เกเฮนน่า",(8.5,11.5),"#000000","https://img2.pic.in.th/pic/9f10c253aacb807c301ab596e8076f7a.png"), 
]

# เมื่อบอทพร้อมทำงาน
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        bot.load_extension("Component.music")
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
    
    boss_names = [boss.name for boss in minibosses]

    for boss_name in boss_names:
        if boss_name in message.content:
            parts = message.content.split()
            if len(parts) >= 2 and parts[0] == boss_name:
                death_time = parts[1]  
                await create_miniboss(message.channel, boss_name, death_time)

    await bot.process_commands(message)
    
    if message.channel.id == GR_channel_id and message.content.isdigit():
        number = int(message.content.replace(',', ''))  # ลบคอมม่า
        username = message.author.display_name
        previous_value = get_previous_value(username)
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
                embed.set_footer(text="SweetDessert GR | ขอบคุณที่ใช้งาน!", icon_url=icon)
                
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
    
    await bot.process_commands(message)

def get_previous_value(username):
    # ฟังก์ชันนี้จะต้องไปดึงค่าจาก Google Sheets เพื่อหาค่าที่เก่าก่อนหน้านี้
    response = requests.get(url + '?username=' + username)
    if response.status_code == 200:
        data = response.json()
        return data.get('GR_value')  # ค่าที่เก่าจะต้องอยู่ในฟิลด์นี้
    return None

async def create_miniboss(channel, boss_name, death_time):
    miniboss_found = next((boss for boss in minibosses if boss.name.lower() == boss_name.lower()), None)
    if miniboss_found:
        await miniboss_found.spawn(death_time, channel)
    else:
        await channel.send("ไม่พบชื่อบอสที่กรอก กรุณาลองใหม่อีกครั้ง.")


@bot.command(name='บอส')
async def miniboss_list(ctx):
    embed = discord.Embed(
        title="📜 รายชื่อบอสและระยะเวลาการเกิด",
        description="นี่คือรายชื่อบอสทั้งหมดที่มีในระบบ:",
        color=discord.Color.blue() 
    )

    # วนลูปเพื่อสร้างข้อมูลบอส
    for boss in minibosses:
        spawn_time_range = f"⏰ {boss.spawn_time_range[0]} - {boss.spawn_time_range[1]} ชั่วโมง"
        embed.add_field(name=f"🦹‍♂️ {boss.name}", value=spawn_time_range, inline=False)

    embed.set_footer(text="ขอบคุณที่ใช้งาน! 😊", icon_url=icon)  # แสดงข้อความท้าย

    # ส่ง Embed
    await ctx.send(embed=embed)



@bot.tree.command(name='rank', description='แสดง rank ของคนมี HSOA')
async def rankcommand(interaction):
    await interaction.response.send_message(rank.rank_numbers())

@bot.tree.command(name='boss',description='แสดงบอสทั้งหมดใน BF1 BF2' )
async def bosscommand(interaction):
    await interaction.response.send_message(miniboss_list())

if __name__ == "__main__":
    flask_thread = Thread(target=server_on)
    flask_thread.start()
    bot.run(os.getenv('TOKEN'))
