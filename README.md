# DiscordEmoteBot

A Quick Discord Emote Adding Bot!

Given a message with a flag a user with permissions to create expressions can then make it into an emote with a quick message

## 
# Instructions
1. Send a message with "$add" and the image you would like to turn into an emote

2. Send command: /emotify <name>

##
# Current Issues

- Needs explicit create expression on top role. cannot inherited
- No testing on the too many emojis case
- only tested for png and jpg
- Tune image cropping 
- Work with discord command auto complete
- Check security for multiple discord servers
- Probably suboptimal python practices, this was a quick one night python derusting project as well as for me to familiarize myself with the discord api


##
# Setup
- Install Docker and Pull the Alpine container
- cd into the main directory in the repo
- run ``` docker build --build-arg TOKEN=$(grep TOKEN .env | cut -d '=' -f2) -t discordemotebot . ```
- to start run ```docker run discordemotebot```
