from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from contextlib import asynccontextmanager
import requests
import json
import os
import uvicorn

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
API_URL = "https://lsb.dev.design.ru/api/v1/"

application = Application.builder().token(BOT_TOKEN).build()

def setup_handlers():
    async def start(update: Update, context):
        options = get_voting_options()
        if not options:
            await update.message.reply_text("Failed to load voting options. Please try again later.")
            return

        keyboard = []
        for i in range(0, len(options), 2):
            row = [
                InlineKeyboardButton(option["name"], callback_data=f"vote_{option['id']}")
                for option in options[i:i+2]
            ]
            keyboard.append(row)

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("За кого голосуем:", reply_markup=reply_markup)

    async def button_handler(update: Update, context):
        query = update.callback_query
        await query.answer()

        user = update.effective_user
        button_data = query.data
        option_id = button_data.replace("vote_", "")

        payload = {
            "action": "battle.setVote",
            "user": option_id,
            "score": 5,
            "login": user.id
        }
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            await query.edit_message_text(text="Голос принят.")
        else:
            await query.edit_message_text(text="Голос уже отдан.")

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

def get_voting_options():
    response = requests.get(f"{API_URL}?action=battle.getList")
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch options", response.text)
        return []

@asynccontextmanager
async def lifespan(app: FastAPI):
    await application.initialize()
    setup_handlers()
    await application.start()

    webhook_url = f"{WEBHOOK_URL}/{BOT_TOKEN}"
    response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook", params={"url": webhook_url})
    if response.status_code == 200:
        print("Webhook set successfully!")
    else:
        print("Failed to set webhook:", response.text)

    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def hello(request: Request):
    return {"hello": "world"}

@app.post(f"/{BOT_TOKEN}")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)

    await application.process_update(update)
    return {"status": "ok"}
