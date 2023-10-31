from dotenv import load_dotenv
from discord.ext import commands
import discord
import os

# Load environment variables from .env file
load_dotenv()
token = os.getenv('TOKEN')

# init intents
intents = discord.Intents.default()
intents.emojis_and_stickers = True
intents.guild_messages = True
intents.guild_reactions = True
intents.message_content = True
global most_recent
bot = commands.Bot(command_prefix='/', intents=intents)

# event: when the bot is ready
@bot.event
async def on_ready():
    print('We have logged in')

# event: look for the most recent image with the caption "&add" and set as most recent
# @bot.event
# async def on_message(m):
#     if m.content == "$add":
#         if len(m.attachments) == 1: 
#             if m.attachments[0].content_type[0:5] == "image/":
#                 most_recent = m
#                 print(most_recent)
#     await bot.process_commands(m) 
@bot.event
async def on_message(m):
    if m.content.startswith("$add"):
        if len(m.attachments) == 1:
            if m.attachments[0].content_type.startswith("image/"):
                global most_recent
                most_recent = m
                print(most_recent)
    await bot.process_commands(m)

# command: status
@bot.command()
async def status(ctx):
    await ctx.send('Active')

# command: add
@bot.command()
async def emotify(ctx, name):
    image = None
    if ctx.author.top_role.permissions.create_expressions: #NEEDS TO EXPLICITLY HAVE MANAGE_EMOJIS, CANNOT BE INHERITED
        if most_recent != None: #is a message
            image = await most_recent.attachments[0].read()
    else: 
       await ctx.send('Either no Emoji Permissions or there is no valid emote candidate')

    guild_emojis = await ctx.guild.fetch_emojis()

    if len(guild_emojis) >= ctx.guild.emoji_limit:
       await ctx.send('Too many Emojis, no more space!')
       return 
    
    if image != None:
        await ctx.guild.create_custom_emoji(name=name, image=image)

bot.run(token)
