import telebot
import re
from collections import Counter

# O'zingizning bot token kodini mana shu yerga qo'shtirnoq ichiga yozing!
API_TOKEN = '8581856443:AAFRrZsUIYk3qxhdRIOM-eTWNQ3O7-dLa48' 

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Menga rulonlar ro'yxatini yuboring, men ularni aniq hisoblab beraman.")

@bot.message_handler(func=lambda message: True)
def calculate_rolls(message):
    text = message.text
    lines = text.strip().split('\n')
    
    total_rolls = 0
    total_sum = 0
    roll_values = []
    
    for line in lines:
        if "rulon" in line.lower():
            match = re.findall(r'\d+', line)
            if len(match) >= 2:
                value = int(match[-1])
                total_sum += value
                total_rolls += 1
                roll_values.append(value)

    if total_rolls == 0:
        bot.reply_to(message, "Iltimos, ro'yxatni to'g'ri formatda yuboring (masalan: 1-rulon 400).")
        return

    counts = Counter(roll_values)
    details = ""
    
    for size, count in sorted(counts.items(), reverse=True):
        category_sum = size * count
        details += f"🔹 **{size} talik:** {count} ta ➡️ Jami: **{category_sum}**\n"

    response = (
        f"📊 **YAKUNIY HISOBOT**\n\n"
        f"🔢 **Jami rulonlar soni:** {total_rolls} ta\n"
        f"📐 **Hammasining umumiy summasi (Jami):** {total_sum}\n\n"
        f"🗂 **O'lchamlar bo'yicha alohida jami:**\n{details}"
    )
    
    bot.reply_to(message, response, parse_mode="Markdown")

if __name__ == "__main__":
    bot.polling(none_stop=True)
