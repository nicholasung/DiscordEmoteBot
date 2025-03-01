from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageOps
from PIL import *
import io
import discord
import os

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
# imgbot = commands.Bot(command_prefix=';', intents=intents)
bot = commands.Bot(command_prefix=';', intents=intents) #discord.Client(intents=intents)


def check_key(key): #return the pair of the guild with most recent
    for pair in most_recent:
        if key == pair.get("gid"):
            print("found")
            return pair
    print("no pair")
    return -1

@bot.event
async def on_message(m):
    if m.content.startswith("/image"):
        if len(m.attachments) == 1:
            if m.attachments[0].content_type.startswith("image/"):
                if len(most_recent) != 0:
                     for i in range(len(most_recent)):
                        if i < len(most_recent) and m.guild.id == most_recent[i].get("gid"):
                            most_recent.pop(i)
                most_recent.append(dict(gid = m.guild.id, msg = m)) #add a new most recent: Must now find a way to delete old recents for the guild if they exist (just have it delete on a timer)
                await m.channel.send("Image is cached in my cheeks!")
            print(most_recent)
    await bot.process_commands(m)


@bot.tree.command(name="status", description="Check the bot's status")
async def status(interaction: discord.Interaction):
     await interaction.response.send_message('Squeak! (I am here!)', ephemeral=True)


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
@bot.tree.command(name="emotify", description="makes the most recent $add image into an emote")
async def emotify(interaction: discord.Interaction, name: str):
    image = None
    if interaction.user.guild_permissions.manage_emojis_and_stickers: #NEEDS TO EXPLICITLY HAVE MANAGE_EMOJIS, CANNOT BE INHERITED
        if check_key(interaction.guild.id) != -1: #is a message put this in a try catch
            image = await check_key(interaction.guild.id).get("msg").attachments[0].read()
        else: 
            # await interaction.response.send_message('There is no valid emote candidate')
            await interaction.response.send_message('Image Error')
    else: 
       await interaction.response.send_message('You do not have emoji creation permissions')

    guild_emojis = await interaction.guild.fetch_emojis() #emjoi limit checks

    if len(guild_emojis) >= interaction.guild.emoji_limit: 
       await interaction.response.send_message('Too many Emojis, no more space!')
       return 

    if image_valid(image):
        # implementing so it is always compressed
        compressed = await compress(image)
        await interaction.guild.create_custom_emoji(name=name, image=compressed) #create emoji
        #await ctx.guild.create_custom_emoji(name=name, image=image_process(image)) #create emoji
        await interaction.response.send_message('Attempted Add :' + name + ':')
    else:
        # await interaction.response.send_message('Image too large (max 250kb)')
        await interaction.response.send_message('Image Error')

# event: when the bot is ready
@bot.event
async def on_ready():
    await bot.tree.sync()
    print('We have logged in and synced')
    print('Synced commands:')
    for command in bot.tree.walk_commands():
        print(f"- {command.name}: {command.description}")

bot.run(token)