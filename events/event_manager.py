from discord.ext import commands, tasks
from helpers.time_utils import parse_duration_from_title, calculate_end_time, dt
from config import CHANNEL_ID, GUILD_ID
from helpers.error_handler import send_log_message

class EventManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manage_events_task.start()

    @tasks.loop(minutes=1)
    async def manage_events_task(self):
        """Background task to manage starting and ending events."""
        await self.bot.wait_until_ready()  # Ensure bot is ready before running the task
        try:
            await self.manage_events()
        except Exception as e:
            error_message = f"An error occurred in the background task: {e}"
            print(error_message)  # Debug print
            await send_log_message(error_message)

    async def manage_events(self):
        """Check events and manage them based on their start and end times."""
        guild = self.bot.get_guild(GUILD_ID)
        if not guild:
            error_message = "Guild not found"
            print(error_message)  # Debug print
            await send_log_message(error_message)
            return

        now = dt.utcnow()

        # Fetch all scheduled events
        existing_events = await guild.fetch_scheduled_events()

        for event in existing_events:
            start_time = event.scheduled_start_time
            duration_days = parse_duration_from_title(event.name)
            end_time = calculate_end_time(start_time, duration_days)

            if start_time <= now < end_time:
                # Event should be active
                await self.start_event(event)

            if now >= end_time:
                # Event should be removed
                await self.remove_event(event)

    async def start_event(self, event):
        """Logic to start an event (e.g., announce it in a channel)."""
        channel = self.bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(f"The event {event.name} is starting now!")
            log_message = f"Event {event.name} has started."
            await send_log_message(log_message)
        else:
            error_message = f"Channel {CHANNEL_ID} not found for event announcement."
            print(error_message)  # Debug print
            await send_log_message(error_message)

    async def remove_event(self, event):
        """Logic to remove an event."""
        await event.delete()
        log_message = f"Event {event.name} has been removed."
        print(log_message)  # Debug print
        await send_log_message(log_message)

async def setup(bot):
    await bot.add_cog(EventManager(bot))
