import random
import asyncio
import discord
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import io
from discord.ext import commands
from sympy import *
from pixabay import get_image as get_img_pixa
intents = discord.Intents.all()

client = commands.Bot(command_prefix='!',intents=intents,add_help=False)

@client.command()
async def get_images(ctx, search_term):

    img_urls = get_img_pixa(search_term)

    if not img_urls:
        await ctx.send(f"No images found for {search_term}")
    else:
        # Send a random image URL to the user
        random_image_url = random.choice(img_urls)
        await ctx.send(random_image_url)

@client.command()
async def customhelp(ctx):
    help_command = client.get_command('help')
    await ctx.send_help(help_command)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    channel = client.get_channel(1075395333082849280)
    url = "https://unsplash.com/fr/s/photos/napoleon"  # Replace with the URL of the website that you want to get the random image from
    while True:
        # await send_random_image(channel, url)
        await asyncio.sleep(60)
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command! Type `!help` to see the available commands.")

@client.event
async def on_message(message):
    print("CHANNEL :",message.channel.name ,"CONTENT:",message.content)
    if message.author == client.user:
        return

    if message.channel.name != "test": # replace with the name of your channel
        return
    content = message.content
    if not content:
        if message.attachments:
            attachment = message.attachments[0]
            content = await attachment.read()

    if message.content.startswith("!solve"):
        expr = message.content[7:]
        try:
            result = str(simplify(expr))
        except Exception as e:
            result = str(e)

        code_block = f"```\n= {result}\n```"
        await message.channel.send(code_block)
    if message.content.startswith('!python '):
        code = message.content[8:]
        try :
            if message.attachments.size > 0:
                print(message.attachements)
                print("There is an attachment")
            else:
                print("There is no attachment")
        except:
            pass
        try:
            output = io.StringIO()
            exec(code, {}, {'print': lambda x: output.write(str(x) + '\n')})
            result = output.getvalue()
            output.close()
            await message.add_reaction("✔")
            await message.channel.send(f"```py\n=> {result}```")
        except:
            pass
    if message.content.startswith('!search'):
        # Get the search term from the message content
        search_term = message.content.split(' ')[1]

        # Invoke the "get_images" command with the search term as the argument
        ctx = await client.get_context(message)
        await ctx.invoke(client.get_command('get_images'), search_term=search_term)

client.run('MTA3NTMyNTg4NzU4MDQ3OTUzOQ.GATqGg.HVeZSMjU40qSnWicnqEdd1U89m7yQSx01RxYQg')