from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageOps
from PIL import *
import io
import discord
import os
import sys

# Load environment variables from .env file
load_dotenv()
token = os.getenv('TOKEN')
print(token)

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

#image valid helper
def image_valid(img):
    if img == None:
        return False
    # if img sys.getsizeof(img) >= 256000:
    # call compression helper and return true
    # if sys.getsizeof(img) < 256000:
    #     return True
    return True

async def compress(b_img):
    # MAIN FUNCTION THAT CALLS HELPERS THAT WILL CONVERT BYTE TO PIL IMG, COMPRESS AND THEN RETURN THE COMPRESSED AS A BYTES OBJECT AGAIN
    p_img = Image.open(io.BytesIO(b_img))
    # compress image 128*128 (integer scale for discord) 
    emote_resolution = (128, 128)
    comp_img = ImageOps.fit(p_img, emote_resolution)
    # convert comp_img to byte string
    comp_b_img = io.BytesIO()
    comp_img.save(comp_b_img, format='PNG')
    return comp_b_img.getvalue()

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

    if image_valid(image):
        # implementing so it is always compressed
        compressed = await compress(image)
        await ctx.guild.create_custom_emoji(name=name, image=compressed) #create emoji
        #await ctx.guild.create_custom_emoji(name=name, image=image_process(image)) #create emoji
        await ctx.send('Attempted Add')
    else:
        await ctx.send('Image too large (max 250kb)')

bot.run(token)
