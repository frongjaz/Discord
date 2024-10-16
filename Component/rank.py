# Component/rank.py
user_numbers = []

def rank_numbers():
    if len(user_numbers) == 0:
        return "No Data"

    sorted_users = sorted(user_numbers, key=lambda x: x['number'], reverse=True)
    message = "อันดับคนมีตราใหญ่ (Rank HSOA) :\n"

    for index, user in enumerate(sorted_users):
        message += f"{index + 1}. {user['username']}: {user['number']}\n"

    return message

def add_user(username, number):
    # เช็คว่าผู้ใช้มีอยู่ใน user_numbers หรือไม่
    for user in user_numbers:
        if user['username'] == username:
            old_number = user['number']  # เก็บค่าตัวเลขเดิม
            user['number'] = number  # แทนที่ตัวเลขเก่าด้วยตัวเลขใหม่
            
            return old_number, True  # คืนค่าตัวเลขเก่าและบอกว่ามีผู้ใช้

    # ถ้าผู้ใช้ไม่มีใน user_numbers ให้เพิ่มใหม่
    user_numbers.append({'username': username, 'number': number})
    return None, False  # คืนค่า None และบอกว่าไม่มีผู้ใช้
