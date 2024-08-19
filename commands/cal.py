from discord.ext import commands
from helpers.event_utils import (
    create_or_update_discord_event,
    parse_json_to_events,
    parse_json_string,
    send_scheduled_event_embed,
)
from helpers.error_handler import handle_command_error, handle_event_creation_error, send_log_message
from config import LOG_CHANNEL_ID

class CalCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cal(self, ctx, *, json_str: str):
        await ctx.send("Processing...")
        """Handle the !cal command to create events from JSON string."""
        try:
            await send_log_message(f"Received JSON string: {json_str}")  # Debugging
            json_data = parse_json_string(json_str)
            await send_log_message(f"Parsed JSON data: {json_data}")  # Debugging
            events_data = parse_json_to_events(json_data)

            if not events_data:
                await ctx.send("No events were found in the provided JSON.")
                return

            for event_data in events_data:
                try:
                    await create_or_update_discord_event(
                        self.bot, ctx.guild.id, event_data
                    )
                    await ctx.send(f"Event created/updated: {event_data['description']}")
                except Exception as e:
                    await send_log_message(f"An error occurred while creating/updating the event: {e}")
                    await handle_event_creation_error(
                        ctx, e, self.bot, ctx.guild.id, ctx.channel.id, event_data
                    )

            # Post calendar embed
            await send_scheduled_event_embed(ctx, json_data)

        except Exception as error:
            await send_log_message(f"An unexpected error occurred: {error}")
            await handle_command_error(ctx, error)

async def setup(bot):
    await bot.add_cog(CalCommand(bot))
