import os
import random
import discord
from discord.ext import commands, tasks
from myserver import server_on  # Assuming this starts your server
from discord import app_commands
from threading import Thread
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

user_numbers = []
target_channel_id = 1290924217184948236
SweetDessert_role = 1218124815378940035

# Function to rank numbers
def rank_numbers():
    if len(user_numbers) == 0:
        return "No Data"

    sorted_users = sorted(user_numbers, key=lambda x: x['number'], reverse=True)
    message = "อันดับคนมีตราใหญ่ (Rank HSOA) :\n"

    for index, user in enumerate(sorted_users):
        message += f"{index + 1}. {user['username']}: {user['number']}\n"

    return message
    
def get_random_welcome_message(member):
    messages = [
        f"ยินดีต้อนรับสู่ SweetDessert, {member.mention}! หวังว่าคุณจะสนุกกับการอยู่ที่นี่ 🍰",
        f"ขอต้อนรับคุณ {member.mention} เข้าสู่ชุมชนของเรา! หวังว่าคุณจะพบเจอเพื่อนใหม่มากมาย 🧁",
        f"Hey {member.mention}, welcome to SweetDessert! เรามีขนมให้ลองเต็มไปหมด 🍮",
    ]
    return random.choice(messages)

# เมื่อบอทพร้อมทำงาน
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    # ซิงค์คำสั่ง Application Command เฉพาะเมื่อมีการเพิ่มคำสั่งใหม่
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")
    
    # เริ่มการแจ้งเตือนทุกวันศุกร์
    friday_reminder.start()

# เมื่อมีสมาชิกเข้าร่วม
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1218562161966841897)
   
    if channel is not None:
        # แท็กผู้ใช้ด้วยการ mention ก่อน
        await channel.send(f"{member.mention} ยินดีต้อนรับ!")

        # สร้าง Embed ที่มีการปรับแต่งมากขึ้น
        embed = discord.Embed(
            title="🎉 ยินดีต้อนรับสู่ SweetDessert! 🎉",
            description=get_random_welcome_message(member),
            color=discord.Color.purple()
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="หวังว่าคุณจะสนุกกับการอยู่ที่นี่! 🍨", icon_url="https://i.imgur.com/ZdfJpK4.png")

        # ส่ง Embed พร้อมปุ่ม
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="เลือก Role", url="https://discord.com/channels/1217800795177750618/1260117726861721620", style=discord.ButtonStyle.link))

        await channel.send(embed=embed, view=view)
    else:
        print("ไม่พบช่องที่ระบุสำหรับการต้อนรับสมาชิกใหม่")

# ฟังก์ชันแจ้งเตือนทุกวันศุกร์
@tasks.loop(time=datetime.utcnow().replace(hour=9, minute=0, second=0))  # แจ้งเตือนเวลา 9:00 UTC (หรือ 16:00 น. ในประเทศไทย)
async def friday_reminder():
    current_day = datetime.utcnow().weekday()
    if current_day == 4:  # ถ้าวันนี้คือวันศุกร์ (Friday = 4)
        channel = bot.get_channel(target_channel_id)
        if channel is not None:
            mention_role = f"<@&{SweetDessert_role}>"
            await channel.send(f"{mention_role} กรุณากรอกตราใหญ่ (HSOA) ของคุณภายในวันนี้!")
        else:
            print("ไม่พบช่องที่ระบุสำหรับการแจ้งเตือน")

# เมื่อมีข้อความส่งมา
@bot.event
async def on_message(message):
    global user_numbers

    if message.author.bot:
        return

    # ฟังก์ชันจัดการกับการพิมพ์ตัวเลขในช่องที่กำหนด
    if message.channel.id == target_channel_id and message.content.isdigit():
        number = int(message.content)
        username = message.author.display_name
        
        # ตรวจสอบว่าผู้ใช้อยู่ในรายการ user_numbers แล้วหรือไม่
        user_exists = False
        for user in user_numbers:
            if user['username'] == username:
                old_number = user['number']  # เก็บค่าตัวเลขเดิม
                user['number'] = number  # แทนที่ตัวเลขเก่าด้วยตัวเลขใหม่
                user_exists = True
                
                # คำนวณการเปลี่ยนแปลงและเปอร์เซ็นต์
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
                break

        # ถ้าผู้ใช้ยังไม่อยู่ในรายการ ให้เพิ่มใหม่และแสดงข้อความแรก
        if not user_exists:
            user_numbers.append({'username': username, 'number': number})
            await message.channel.send(f"คุณ {username} มีตราใหญ่ (HSOA) : {number}")

    # แสดงอันดับ HSOA
    if message.content.lower() == '!rank':
        ranking_message = rank_numbers()
        await message.channel.send(ranking_message)

    # Reset ข้อมูล
    if message.content.lower() == '!clear':
        user_numbers = []
        await message.channel.send("Clear เรียบร้อย!")

@bot.tree.command(name='rank', description='แสดง rank ของคนมี HSOA')
async def rankcommand(interaction):
    await interaction.response.send_message(rank_numbers())

# Start the bot and the server concurrently
if __name__ == "__main__":
    # Run the Flask server in a separate thread
    flask_thread = Thread(target=server_on)
    flask_thread.start()

    # Start the Discord bot
    bot.run(os.getenv('TOKEN'))
