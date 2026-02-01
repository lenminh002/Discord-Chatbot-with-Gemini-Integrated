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

async def chat_with_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        config={
            "system_instruction": "You are a helpful assistant.",
            "max_output_tokens": 2000
        },
        contents=prompt,
    )
    
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
    # Lmao UserID
    specialMember1 = message.guild.get_member(338993997060112395) 
    # My UserID
    specialMember2 = message.guild.get_member(703141119554355210)
    if message.author == bot.user:
        return


    if 'help' in message.content.lower():
        await message.channel.send(f"Hello {message.author.mention}, how can I assist you? Ping {bot.user.mention} hello to get started!")
    
    elif 'who is the gayest person that is ever existed' in message.content.lower():
        await message.channel.send(f"That would be {specialMember1.mention}!")
    
    elif 'who is the most handsome man here' in message.content.lower():
        await message.channel.send(f"That would be {specialMember2.mention}!")

    else:
        try:
            if bot.user in message.mentions:
                gemini_response = await chat_with_gemini(message.content)
                await message.channel.send(gemini_response)
        except Exception as e:
            print(f"Error with Gemini API: {e}")


    await bot.process_commands(message)



bot.run(token, log_handler=handler, log_level=logging.DEBUG)
