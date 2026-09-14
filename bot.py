import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

BOT_NAME = "Starz Promosyon"

WELCOME_TEXT = (
    "✨ Welcome to Starz Promosyon!\n\n"
    "Explore fashion, clothing, and the latest special offers.\n\n"
    "👕 Fashion & clothing\n"
    "🔥 New promotions\n"
    "✨ Fresh styles & updates"
)


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 Promotions", callback_data="promotions")],
        [InlineKeyboardButton("✨ About Starz", callback_data="about")],
        [InlineKeyboardButton("📞 Contact Us", callback_data="contact")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME_TEXT, reply_markup=main_menu())


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "promotions":
        text = "🔥 Latest Promotions\n\nNew fashion offers and updates will appear here soon."
    elif query.data == "about":
        text = "✨ Starz Promosyon\n\nFashion, style & special offers — all in one place."
    else:
        text = "📞 Contact Us\n\nThanks for your interest in Starz Promosyon."

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Back", callback_data="back")]
        ]) if query.data != "back" else main_menu(),
    )

    if query.data == "back":
        await query.edit_message_text(WELCOME_TEXT, reply_markup=main_menu())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Use /start to open the Starz Promosyon menu.")


def run() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is not set.")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    run()
