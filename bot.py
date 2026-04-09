import os
from flask import Flask, request
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# ===== CONFIG =====
TOKEN = os.getenv("BOT_TOKEN")  # Set your bot token in Render ENV
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # Your Telegram ID

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ===== MESSAGES =====
start_message = """⚠️ Disclaimer

This bot is created for educational purposes only.
Trading involves financial risk and may result in losses.

We do not provide financial advice, signals, or guaranteed outcomes.

All content is for learning and informational use only.
These are projections and not guarantees.

By continuing, you confirm that you understand and accept this.

👋 Welcome to Market learner Bot!

Use the buttons below to start exploring a topic:
"""

topics = {
"📘 Market Mindset": """📘 Market Mindset

Concept: Your mindset is the foundation of trading success. Calm, structured thinking reduces impulsive mistakes and helps you make decisions based on logic rather than emotion.

Key Points:

1. Recognize Emotional Triggers: Fear, greed, and FOMO often cause impulsive decisions.

2. Pause Before Acting: Ask: “Why am I entering this trade? What is my goal?”

3. Reflect on Past Decisions: Keep a trading journal to analyze mistakes and successes.

4. Plan for Uncertainty: Accept that not all market moves are predictable.

Example:
Price spikes sharply. A reactive trader might buy immediately. A mindful trader:

Observes trend & volume

Checks support/resistance levels

Decides calmly based on risk tolerance

Outcome:
Structured thinking improves patience, decision-making, and confidence over time.

⚠️ This content is for educational purposes only.
“These are projections and not guarantees.”
""",
"📈 Trend Analysis": """📈 Trend Analysis

Concept: Trends represent the general direction of the market and help you plan entries and exits with more certainty.

Key Points:

1. Identify Trend Direction: Higher highs/lows → uptrend, lower highs/lows → downtrend.

2. Use Indicators: Moving averages filter noise. Volume confirms trend strength.

3. Recognize Trend Changes: Reversals, breakouts, divergence signal trend weakening.

Example:
Market forms higher highs → upward trend → wait for small pullback to buy instead of chasing.

Outcome:
Trend recognition prevents overtrading and aligns trades with market movement.

⚠️ This content is for educational purposes only.
“These are projections and not guarantees.”
""",
"⚖️ Smart Risk Allocation": """⚖️ Smart Risk Allocation

Concept: Protecting your capital is as important as making profits. Smart risk management ensures long-term survival.

Key Points:

1. Limit Risk per Trade: 1–2% of total capital per trade.

2. Set Stop-Loss & Take-Profit: Pre-define exit points.

3. Diversify Positions: Spread capital across multiple trades.

4. Adjust Risk to Market Volatility: More volatile markets → tighter control.

Example:
$2000 capital, risking $20 per trade. Diversifying across crypto & stocks spreads risk.

Outcome:
Reduces stress, builds confidence, allows consistent progress.

⚠️ This content is for educational purposes only.
“These are projections and not guarantees.”
""",
"🧠 Emotional Control": """🧠 Emotional Control

Concept: Emotional discipline separates successful traders from impulsive ones.

Key Points:

1. Follow Your Trading Plan: Stick to rules.

2. Maintain a Trading Journal: Track feelings & mistakes.

3. Take Breaks: Avoid stress in volatile markets.

4. Practice Patience: Wait for high-probability setups.

Example:
Market drops suddenly. Fearful trader sells immediately. Disciplined trader evaluates trend & risk calmly.

Outcome:
Reduces impulsive losses, builds confidence and consistency.

⚠️ This content is for educational purposes only.
“These are projections and not guarantees.”
""",
"🔍 Technical Patterns": """🔍 Technical Patterns

Concept: Chart patterns help anticipate price movements and identify opportunities.

Key Points:

1. Head & Shoulders: Trend reversal.

2. Double Top/Bottom: Strong support/resistance.

3. Triangles: Show potential breakout directions.

4. Candlestick Patterns: Insight into market sentiment.

5. Confirm Patterns with Volume: Patterns without volume are less reliable.

Example:
Stock forms double bottom near $50 → likely to rise → plan entry with stop-loss & candlestick confirmation.

Outcome:
Structured analysis, reduced guesswork, higher probability trades.

⚠️ This content is for educational purposes only.
“These are projections and not guarantees.”
""",
"❓ FAQ": """❓ FAQ

Q: Is this bot giving financial advice?
A: No. All content is educational. You are responsible for your own trades.

Q: Will I make guaranteed profits?
A: No. Trading involves risk. Past performance ≠ future results.

Q: Can beginners use this bot?
A: Yes. Start with Market Mindset and move step by step.

Q: How often is new content added?
A: Lessons & mini-quizzes are updated regularly.

Q: What if I make a mistake in trading?
A: Mistakes are part of learning. Use journals, risk management & emotional control.

⚠️ This content is for educational purposes only.
“These are projections and not guarantees.”
"""
}

# ===== KEYBOARD =====
def get_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [KeyboardButton(name) for name in topics.keys()]
    markup.add(*buttons)
    return markup

# ===== HANDLERS =====
@bot.message_handler(commands=['start'])
def start(message):
    # 1️⃣ Send disclaimer and pin it
    try:
        msg = bot.send_message(message.chat.id, start_message)
        bot.pin_chat_message(message.chat.id, msg.message_id, disable_notification=True)
    except:
        pass

    # 2️⃣ Send welcome message + keyboard
    bot.send_message(
    message.chat.id,
    """👋 Welcome to Market learner Bot!

This bot is your step-by-step guide to learning trading markets safely and effectively.
Here, you will explore the following topics:
📘 Market Mindset – Learn how your emotions influence trading and how structured thinking improves decisions.
📈 Trend Analysis – Understand market trends, identify uptrends, downtrends, and sideways markets for better trading.
⚖️ Smart Risk Allocation – Protect your capital with position sizing, stop-loss strategies, and diversification.
🧠 Emotional Control – Master discipline, patience, and avoid impulsive mistakes caused by fear or greed.
🔍 Technical Patterns – Learn key chart patterns and candlestick signals to anticipate potential market moves.
❓ FAQ – Get answers to common questions about trading, risk, and using this bot.

⚠️ This content is for educational purposes only.
“These are projections and not guarantees.”

Use the buttons below to start exploring a topic:

📘 Market Mindset
📈 Trend Analysis
⚖️ Smart Risk Allocation
🧠 Emotional Control
🔍 Technical Patterns
❓ FAQ""",
    reply_markup=get_keyboard()
    )

# Handle topic selection from keyboard
@bot.message_handler(func=lambda message: message.text in topics.keys())
def send_topic(message):
    bot.send_message(message.chat.id, topics[message.text], reply_markup=get_keyboard())

# ===== WEBHOOK / FLASK =====
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Bot is running!"

# ===== RUN =====
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://siva-education-bot-1.onrender.com/{TOKEN}")  # Replace with your Render domain
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
