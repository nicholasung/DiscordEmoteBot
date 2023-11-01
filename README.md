# DiscordEmoteBot

A Quick Discord Emote Adding Bot!

Given a message with a flag a user with permissions to create expressions can then make it into an emote with a quick message

## 
# Instructions
1. Send a message with "$add" and the image you would like to turn into an emote

2. Send command: /emotify <name>

##
# Current Issues

- No testing nor protection for multiple servers. 1 bot per server recommended
- Needs explicit create expression on top role. cannot inherited
- No testing on the too many emojis case
- No testing on oddly shaped images
- No testing on non .png images
- Add image processing to crop into squares
- Work with discord command auto complete
- Probably suboptimal python practices, this was a quick one night python derusting project as well as for me to familiarize myself with the discord api

##
# To Do
- Address current issues
- Pack into Docker


##
# Setup
- Install Python3 and the following dependencies:
  - dotenv 1.0.0
  - discord 2.3.2
- Create a discord bot through their developer website
- Paste in your token in .env
- Run main.py
