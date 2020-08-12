# bot.py
import os

import discord
from discord import Client
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client: Client = discord.Client()

@client.event
async def on_ready():
     print(f'{client.user} has connected to Discord!')

client.run(TOKEN)

