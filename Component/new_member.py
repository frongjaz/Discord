import random
import discord

# ฟังก์ชันต้อนรับสมาชิกใหม่
async def on_member_join(bot, member):
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

# ฟังก์ชันสุ่มข้อความต้อนรับ
def get_random_welcome_message(member):
    messages = [
        f"ยินดีต้อนรับสู่ SweetDessert, {member.mention}! หวังว่าคุณจะสนุกกับการอยู่ที่นี่ 🍰",
        f"ขอต้อนรับคุณ {member.mention} เข้าสู่ชุมชนของเรา! หวังว่าคุณจะพบเจอเพื่อนใหม่มากมาย 🧁",
        f"Hey {member.mention}, welcome to SweetDessert! เรามีขนมให้ลองเต็มไปหมด 🍮",
    ]
    return random.choice(messages)
