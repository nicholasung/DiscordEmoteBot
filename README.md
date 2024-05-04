# DiscordEmoteBot

A Quick Discord Emote Adding Bot!

Given a message with a flag a user with permissions to create expressions can then make it into an emote with a quick message

## 
# Instructions
1. Send a message with "$add" and the image you would like to turn into an emote

2. Send command: /emotify <name>

##
# Setup
- Install Docker and Pull the Alpine container
- cd into the main directory in the repo
- Add your bots token to the .env file
- run ``` docker build --build-arg TOKEN=$(grep TOKEN .env | cut -d '=' -f2) -t discordemotebot . ```
- to start run ```docker run discordemotebot```
