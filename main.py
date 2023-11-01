from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
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
most_recent = [] #array of dictionary pairs (guild, message)
bot = commands.Bot(command_prefix='/', intents=intents)

# event: when the bot is ready
@bot.event
async def on_ready():
    print('We have logged in')

def check_key(key): #return the pair of the guild with most recent
    for pair in most_recent:
        if key == pair.get("gid"):
            print("found")
            return pair
    print("no pair")
    return -1
        


@bot.event
async def on_message(m):
    if m.content.startswith("$add"):
        if len(m.attachments) == 1:
            if m.attachments[0].content_type.startswith("image/"):
                if len(most_recent) != 0:
                     for i in range(len(most_recent)):
                        if i < len(most_recent) and m.guild.id == most_recent[i].get("gid"):
                            most_recent.pop(i)
                most_recent.append(dict(gid = m.guild.id, msg = m)) #add a new most recent: Must now find a way to delete old recents for the guild if they exist (just have it delete on a timer)
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
        if check_key(ctx.guild.id) != -1: #is a message
            image = await check_key(ctx.guild.id).get("msg").attachments[0].read()
        else: 
            await ctx.send('There is no valid emote candidate')
    else: 
       await ctx.send('You do not have emoji creation permissions')

    guild_emojis = await ctx.guild.fetch_emojis() #emjoi limit checks

    if len(guild_emojis) >= ctx.guild.emoji_limit: 
       await ctx.send('Too many Emojis, no more space!')
       return 
    
    if image != None:
        await ctx.guild.create_custom_emoji(name=name, image=image) #create emoji
        ctx.send('Attempted Add')

bot.run(token)
