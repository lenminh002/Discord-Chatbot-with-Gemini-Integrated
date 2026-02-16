Add gemini api key and discord token into .env to work

- run: docker build -t smart_discord_bot .
- run: docker run --env-file .env smart_discord_bot