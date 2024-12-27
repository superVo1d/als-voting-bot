# Voting Bot

A Telegram bot that allows users to vote for options fetched from an external API. The bot displays options as inline keyboard buttons and allows users to vote for their selected option. The bot is implemented using `FastAPI` and `python-telegram-bot`.

## Features

- Displays voting options fetched from an external API.
- Users can vote for options using inline keyboard buttons.
- Webhook integration for real-time updates.

## Configuration

The app requires the following environment variables in a `.env` file:
```
BOT_TOKEN=your-bot-token
WEBHOOK_URL=your-webhook-url
```
Replace `your-bot-token` and `your-webhook-url` with your actual values.

## Launch

To start the bot with Docker Compose, run the following command:
```
docker-compose up --build
```
