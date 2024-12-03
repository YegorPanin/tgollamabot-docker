import aiohttp
import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

bot_key = os.getenv('BOT_KEY')
model_name = os.getenv('MODEL_NAME')
url = 'http://localhost:11434/api/generate'

async def llm_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    payload = {
        "model": model_name,
        "prompt": update.message.text
    }
    message = await update.message.reply_text("...")
    answer = ""

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status == 200:
                async for line in response.content:
                    data = json.loads(line.decode('utf-8'))
                    answer += " " + data.get("response", "")
                await context.bot.edit_message_text(chat_id=update.effective_chat.id, 
                                                    message_id=message.message_id, 
                                                    text=answer)
            else:
                await context.bot.edit_message_text(chat_id=update.effective_chat.id, 
                                                    message_id=message.message_id, 
                                                    text=f'Ошибка сервера: {response.status}')

app = ApplicationBuilder().token(bot_key).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, llm_reply))

app.run_polling()
