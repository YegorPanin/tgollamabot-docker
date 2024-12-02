from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
import asyncio, aiohttp

bot_key = os.getenv('BOT_KEY')
model_name = os.getenv('MODEL_NAME')
url = 'http://localhost:11434/api/generate'

async def llm_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    payload = {
        "model": "hf.co/MTSAIR/Cotype-Nano-GGUF",
        "prompt": update.message.text
    }
    await update.message.reply_text("...")
    answer = "" 
    async with aiohttp.ClientSession as session:
        async with session.post(url, json=payload) as response:
            data = await response.json()
            answer += " " + data["response"]
            await context.bot_edit_message_text(chat_id=update.effective_chat.id, 
            message_id = message.message_id, 
            text=answer)

app = ApplicationBuilder().token(bot_key).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, llm_reply))

app.run_polling()
