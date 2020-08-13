import discord
import os
import numpy as np

client = discord.Client()


# Functions
def evaluate_triggers(trigger, evaluator):
    return any([True for word in trigger if word in evaluator])


# Events
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'Hello there!':
        response = 'GENERAL KENOBI'
        await message.channel.send(response)
