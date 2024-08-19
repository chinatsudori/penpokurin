import discord
import json
import asyncio
from gspread.exceptions import APIError
from helpers.event_utils import create_or_update_discord_event
from config import LOG_CHANNEL_ID

async def send_log_message(self, message):
    log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(message)
    else:
        print(f"Log channel {LOG_CHANNEL_ID} not found.")

# Custom exception for Google Sheets API errors
class GoogleSheetsAPIError(Exception):
    def __init__(self, error_embed):
        self.error_embed = error_embed

# Function to create an error embed
def create_error_embed(error):
    embed = discord.Embed(
        title="Google Sheets API Error",
        description=f"An error occurred: {error}",
        color=discord.Color.red(),
    )
    return embed

# Centralized error handling function
def handle_api_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except APIError as e:
            print(f"Google Sheets API Error: {e}")
            raise GoogleSheetsAPIError(create_error_embed(e))

    return wrapper

async def handle_command_error(ctx, error):
    if isinstance(error, json.JSONDecodeError):
        await ctx.send("Invalid JSON provided.")
        await send_log_message(
            ctx.bot,
            "Command Error",
            f"**Command:** {ctx.command}\n**Error:** Invalid JSON provided",
            discord.Color.red()
        )
    else:
        await ctx.send(f"An unexpected error occurred: {error}")
        await send_log_message(
            ctx.bot,
            "Command Error",
            f"**Command:** {ctx.command}\n**Error:** {error}",
            discord.Color.red()
        )

async def handle_event_creation_error(
    ctx, error, bot, guild_id, channel_id, event_data
):
    """Handle errors during event creation with retry logic."""
    if "rate limited" in str(error):
        retry_after = int(error.split('retry_after": ')[1].split(",")[0])
        await asyncio.sleep(retry_after)
        try:
            created_event = await create_or_update_discord_event(
                bot, guild_id, channel_id, event_data
            )
            await ctx.send(f"Event created after retry: {created_event.name}")
        except Exception as e:
            await ctx.send(f"An error occurred after retry: {e}")
            await send_log_message(
                bot,
                "Event Creation Error",
                f"**Guild ID:** {guild_id}\n**Channel ID:** {channel_id}\n**Event Data:** {event_data}\n**Error:** {e}",
                discord.Color.red()
            )
    else:
        await ctx.send(f"An error occurred: {error}")
        await send_log_message(
            bot,
            "Event Creation Error",
            f"**Guild ID:** {guild_id}\n**Channel ID:** {channel_id}\n**Event Data:** {event_data}\n**Error:** {error}",
            discord.Color.red()
        )
