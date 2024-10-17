from discord.ext import tasks
from datetime import datetime, time
import discord
from datetime import time, datetime
from discord.ext import tasks
from Component.rank import rank_numbers, user_numbers

target_channel_id = 1290924217184948236  # ID ของช่องที่ต้องการส่งข้อความแจ้งเตือน
guild_wallet_id = 811207505631510538  # ID ของกระเป๋าที่จะส่งไป
SweetDessert_role = 1218124815378940035

# ฟังก์ชันแจ้งเตือนวันศุกร์
@tasks.loop(time=time(9, 0))  # 9 utc+0
async def friday_reminder(bot):
    current_day = datetime.utcnow().weekday()
    if current_day == 4:  # ถ้าวันนี้คือวันศุกร์ (Friday = 4)
        
        
        channel = bot.get_channel(target_channel_id)
        if channel is not None:
            mention_role = f"<@&{SweetDessert_role}>"
            await channel.send(f"{mention_role} กรุณากรอกตราใหญ่ (HSOA) ของคุณภายในวันนี้!")
        else:
            print("ไม่พบช่องที่ระบุสำหรับการแจ้งเตือน")  



# แจ้งเตือนคนที่ได้ Rank 1
@tasks.loop(time=time(hour=15, minute=0)) 
async def saturday_reminder(bot):
    current_day = datetime.utcnow().weekday()
    
    if current_day == 5: 
        channel = bot.get_channel(target_channel_id)

        if channel is not None:
            if len(user_numbers) > 0:
                sorted_users = sorted(user_numbers, key=lambda x: x['number'], reverse=True)
                rank1_user = sorted_users[0]  # คนที่ได้ rank 1
                
                # หา object ของ user ที่ได้ rank 1 จาก ID หรือชื่อ
                member = discord.utils.get(channel.guild.members, display_name=rank1_user['username'])

                if member is not None:
                    await channel.send(
                        f"คุณ {member.mention} ได้รับตราใหญ่จากกิลด์ โปรดส่งเลขกระเป๋ามาที่ <@&{guild_wallet_id}>"
                    )
                else:
                    await channel.send("ไม่สามารถหาอันดับ 1 ในเซิร์ฟเวอร์ได้")
            else:
                await channel.send("ยังไม่มีข้อมูลการจัดอันดับ")
        else:
            print("ไม่พบช่องที่ระบุสำหรับการแจ้งเตือน")
