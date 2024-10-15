import os
import random
import discord
from discord.ext import commands
from myserver import server_on  # Assuming this starts your server
from discord import app_commands
from threading import Thread

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

user_numbers = []
target_channel_id = 1290924217184948236

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
    await bot.tree.sync()

# เมื่อมีสมาชิกเข้าร่วม
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1218562161966841897)

    if channel is not None:
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
        view.add_item(discord.ui.Button(label="เลือก Role", url="https://discord.com/channels/123456789012345678/1260117726861721620", style=discord.ButtonStyle.link))

        await channel.send(embed=embed, view=view)
    else:
        print("ไม่พบช่องที่ระบุสำหรับการต้อนรับสมาชิกใหม่")

# เมื่อมีข้อความส่งมา
@bot.event
async def on_message(message):
    global user_numbers  # Declare global variable

    if message.author.bot:
        return

    if message.channel.id == target_channel_id and message.content.isdigit():
        number = int(message.content)
        username = message.author.display_name
        user_numbers.append({'username': username, 'number': number})
        await message.channel.send(f"คุณ {username} มีตราใหญ่ (HSOA) : {number}")

    if message.content.lower() == '!rank':
        ranking_message = rank_numbers()
        await message.channel.send(ranking_message)

    if message.content.lower() == '!clear':
        user_numbers = []
        await message.channel.send("Reset เรียบร้อย!")

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
