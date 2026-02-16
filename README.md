## HOW TO RUN THE BOT

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

