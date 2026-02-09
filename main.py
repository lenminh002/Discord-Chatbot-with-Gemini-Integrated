import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

from google import genai

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
gemini_api_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=gemini_api_key)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

systemInstruction = """
                        You are a concise helpful Discord Bot assistant. 
                        Response must be 2000 or fewer characters since it is the limit for Discord messages.
                        If the answer is long, provide a high-level summary only.
                    """

# bot's brain
message_array = []
async def chat_with_gemini(prompt):

    # add prompt to the message array
    message_array.append({
        "role": "user", 
        "parts": [{"text": prompt}] # Wrap your text in a dictionary inside the list
    })


    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        config={
            "system_instruction": systemInstruction
        },
        contents=message_array,
    )

    
    ai_text = response.text.strip()

    if(len(ai_text) > 2000):
        ai_text = ai_text[:2000] # Truncate to 2000 characters

    # add AI response to the message array
    message_array.append({
        "role": "model", 
        "parts": [{"text": ai_text}]
    })

    if len(message_array) > 20:
        del message_array[:4] # remove the oldest 4 messages (2 user + 2 model) to keep the conversation relevant and concise

    return response.text.strip()


@bot.event
async def on_ready():
    print(f'{bot.user.name} is activated!')
    print('------')

@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server.')
    await member.guild.system_channel.send(f"Hello {member.mention}! Welcome to the server!")

@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server.')
    await member.guild.system_channel.send(f"Goodbye {member.mention}! Hope to see you again soon!")


@bot.event
async def on_message(message):
    
    if message.author == bot.user:
        return
    if bot.user in message.mentions:

        prompt = message.content.replace(f'<@{bot.user.id}>', '').replace(f'<@!{bot.user.id}>', '').strip()

        if not prompt:
            await message.channel.send(f"Hello {message.author.mention}, how can I assist you? Ping {bot.user.mention} hello to get started!")
        else:
            try:
                await message.channel.send(f"{bot.user.mention} is thinking...")
                bot_response = await chat_with_gemini(prompt)
                await message.channel.send(bot_response)

            except Exception as e:
                if "429" in str(e):
                    print("Rate limit exceeded (429).")
                    await message.channel.send("I'm tired! I've hit my rate limit. Please give me a moment to rest and try again soon.")
                else:
                    print(f"Error with Gemini API: {e}")
                    await message.channel.send(f"Error: {e}")


    await bot.process_commands(message)



bot.run(token, log_handler=handler, log_level=logging.INFO)
