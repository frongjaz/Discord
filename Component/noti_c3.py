from discord.ext import tasks
from datetime import datetime, time

# ฟังก์ชันแจ้งเตือนวันศุกร์
@tasks.loop(time=time(9, 0))  # แจ้งเตือนเวลา 9:00 UTC (หรือ 16:00 น. ในประเทศไทย)
async def friday_reminder(bot):
    current_day = datetime.utcnow().weekday()
    if current_day == 4:  # ถ้าวันนี้คือวันศุกร์ (Friday = 4)
        target_channel_id = 1290924217184948236
        SweetDessert_role = 1218124815378940035
        
        channel = bot.get_channel(target_channel_id)
        if channel is not None:
            mention_role = f"<@&{SweetDessert_role}>"
            await channel.send(f"{mention_role} กรุณากรอกตราใหญ่ (HSOA) ของคุณภายในวันนี้!")
        else:
            print("ไม่พบช่องที่ระบุสำหรับการแจ้งเตือน")
