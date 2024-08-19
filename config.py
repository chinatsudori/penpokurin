import os
import discord

# Environment variables
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1102574302114619503
LOG_CHANNEL_ID = 1102574302114619503
CLAN_ROLE_ID = 1102590757199687741
SUPPORT_REQUEST_CHANNEL_ID = 1221944116926222377
EMOTE_CHAN = [1266092232906379285, 1102558718937288717, 1266098331604746311, 1102574302114619503, 1221944116926222377]
GUILD_ID= 134657795726245888
# Bot configuration
COMMAND_PREFIX = "!"
INTENTS = discord.Intents.default()
INTENTS.message_content = True

# Google Sheets configuration
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
CREDS_PATH = "./penpokurin-6af7c80f9063.json"
SHEET = "Origami Clan Tools"
ARCHIVE = "Origami CB count"