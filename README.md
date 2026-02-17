## ABOUT
Your very own Discord Bot that is powered by Gemini 3. 
**How to try?**
Ping the bot's usernane and start the conversation with it.

## HOW TO RUN THE BOT
**Set Up**
1. Go to Discord Developer Portal: https://discord.com/developers/home
2. Go to applications section and press New Application to create your Discord Bot
3. Add your bot to your server
4. Retrieve Discord token

- **Run Locally**
1. Download all the file
2. Create .env file and add gemini api key and discord token into .env to work
3. Run commands:
    1. pip install -r requirements.txt (pip3 for Mac)
    2. python main.py (python3 for Mac)

- **Run with Docker**
1. Download all the file
2. Create .env file and add gemini api key and discord token into .env to work
3. Run commands:
    1. docker build -t smart_discord_bot .
    2. docker run --env-file .env smart_discord_bot

## Future Update:
- Summarize messages
- Voice Chat

