from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "7920410442:AAHYmlXHOKGeeFJ2p7SXkEGmEqTMIz-GICg"
WEBAPP_URL = "https://xoorix.com"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(
            "💳 Choose Payment Method",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]]
    await update.message.reply_text(
        "👋 Welcome! Click below to choose your payment method:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.message.web_app_data.data  # 'cbe' or 'telebirr'

    if data == "cbe":
        text = "🏦 *CBE Bank*\nAccount Name: Your Name\nAccount Number: 1000XXXXXXXX"
    else:
        text = "📱 *Telebirr*\nPhone Number: 09XXXXXXXX\nName: Your Name"

    keyboard = [[
        InlineKeyboardButton("✅ I Paid", callback_data="paid"),
        InlineKeyboardButton("❌ Cancel", callback_data="cancel")
    ]]
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "paid":
        await query.message.reply_text("✅ Payment received! Thank you.")
    elif query.data == "cancel":
        await query.message.reply_text("❌ Cancelled.")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app_data))
app.add_handler(CallbackQueryHandler(handle_buttons))
app.run_polling()