from discord.ext import commands
from helpers.event_utils import (
    create_or_update_discord_event,
    parse_json_to_events,
    parse_json_string,
    send_scheduled_event_embed,
)
from helpers.error_handler import handle_command_error, handle_event_creation_error
from lib.error_handler import setup_logging, log_info, log_error  # Import custom logging functions

class CalCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        setup_logging()  # Setup logging configuration

    @commands.command()
    async def cal(self, ctx, *, json_str: str):
        """Handle the !cal command to create events from JSON string."""
        await ctx.send("Processing...")
        try:
            # Log the received JSON string for debugging purposes
            log_info(f"Received JSON string: {json_str}")  # Use log_info for informational messages
            json_data = parse_json_string(json_str)
            # Log the parsed JSON data for debugging purposes
            log_info(f"Parsed JSON data: {json_data}")  # Use log_info for informational messages
            events_data = parse_json_to_events(json_data)

            if not events_data:
                await ctx.send("No events were found in the provided JSON.")
                return

            for event_data in events_data:
                try:
                    await create_or_update_discord_event(self.bot, ctx.guild.id, event_data)
                    await ctx.send(f"Event created/updated: {event_data['description']}")
                except Exception as e:
                    error_msg = f"Error creating/updating event: {event_data['description']}, Error: {e}"
                    log_error(error_msg, exc_info=True)  # Use log_error for error messages
                    await handle_event_creation_error(ctx, e, self.bot, ctx.guild.id, ctx.channel.id, event_data)

            # Post calendar embed after processing all events
            await send_scheduled_event_embed(ctx, json_data)

        except Exception as error:
            error_msg = f"An unexpected error occurred processing the calendar command: {error}"
            log_error(error_msg, exc_info=True)  # Use log_error for error messages
            await handle_command_error(ctx, error)

async def setup(bot):
    await bot.add_cog(CalCommand(bot))