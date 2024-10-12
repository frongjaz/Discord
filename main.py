import os
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
        embed = discord.Embed(
            title="ยินดีต้อนรับ!",
            description=f"ยินดีต้อนรับคุณ {member.mention} เข้าสู่ **SweetDessert**!\nกรุณาเลือก Role ได้ที่ <#1260117726861721620>",
            color=discord.Color.green()
        )

        embed.set_thumbnail(url=member.display_avatar.url)  # Correct way to get the avatar URL
        embed.set_footer(text="หวังว่าคุณจะสนุกกับการอยู่ที่นี่!")

        await channel.send(embed=embed)
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
