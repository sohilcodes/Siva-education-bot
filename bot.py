import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # 👈 apna Telegram user ID

bot = telebot.TeleBot(BOT_TOKEN)

# ===== USER STORAGE (temporary memory) =====
users = set()

# ===== REPLY KEYBOARD =====
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    
    markup.row(
        KeyboardButton("📘 Trading Basics"),
        KeyboardButton("📊 Market Concepts")
    )
    markup.row(
        KeyboardButton("🧠 Risk Management"),
        KeyboardButton("📈 Chart Education")
    )
    markup.row(
        KeyboardButton("❓ FAQ"),
        KeyboardButton("📩 Contact Support")
    )

    return markup

# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    name = message.from_user.first_name

    # ===== NEW USER CHECK =====
    if user_id not in users:
        users.add(user_id)

        try:
            bot.send_message(
                ADMIN_ID,
                f"🚀 New User Joined!\n\n👤 Name: {name}\n🆔 ID: {user_id}"
            )
        except:
            pass

    text = """⚠️ Disclaimer

This bot is created for educational purposes only.
Trading involves financial risk and may result in loss.
We do not provide financial advice, signals, or guaranteed results.

By continuing, you confirm that you understand and accept this."""

    msg = bot.send_message(message.chat.id, text, reply_markup=main_menu())

    # Auto pin
    try:
        bot.pin_chat_message(message.chat.id, msg.message_id)
    except:
        pass

# ===== BUTTON HANDLER =====
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text

    if text == "📘 Trading Basics":
        reply = """📘 Trading Basics

Trading is the process of buying and selling assets in financial markets.

Key concepts:
• Buy & Sell
• Price movement
• Timeframes
• Candlestick charts"""

    elif text == "📊 Market Concepts":
        reply = """📊 Market Concepts

Markets move based on supply and demand.

• Uptrend – higher highs and higher lows
• Downtrend – lower highs and lower lows
• Range – sideways movement"""

    elif text == "🧠 Risk Management":
        reply = """🧠 Risk Management

• Never risk money you cannot afford to lose
• No strategy works 100%
• Emotional control is important
• Discipline matters more than profit"""

    elif text == "📈 Chart Education":
        reply = """📈 Chart Education

• Candlestick patterns
• Support & resistance
• Indicators (RSI, Moving Average)"""

    elif text == "❓ FAQ":
        reply = """❓ FAQ

Q: Do you provide trading signals?
A: No

Q: Can trading guarantee profit?
A: No"""

    elif text == "📩 Contact Support":
        reply = """📩 Contact Support

For Learn More: @Market_Learner01"""

    else:
        reply = "Please select an option from menu 👇"

    bot.send_message(message.chat.id, reply, reply_markup=main_menu())

# ===== RUN =====
bot.infinity_polling()
