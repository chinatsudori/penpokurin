from discord.ext import commands, tasks
import asyncio
from helpers.time_utils import get_current_time, get_start_of_next_day
from .update_emote_usage import UpdateEmoteUsageTask
from lib.error_handler import log_info, log_error, log_debug  # Import logging functions


class StartScheduledTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_scheduled_task.start()

    @commands.Cog.listener()
    async def on_ready(self):
        log_debug("StartScheduledTask cog and on_ready event triggered.")

    @tasks.loop(hours=24)  # Run every 24 hours
    async def start_scheduled_task(self):
        log_debug("Starting scheduled task.")
        try:
            now = get_current_time()  # Assuming synchronous, remove await if not async
            next_run = (
                get_start_of_next_day()
            )  # Assuming synchronous, remove await if not async
            delay = (next_run - now).total_seconds()
            log_debug(
                f"Current time: {now}, Next run time: {next_run}, Delay: {delay} seconds."
            )
            await asyncio.sleep(delay)
            cog = self.bot.get_cog("UpdateEmoteUsageTask")
            if cog:
                cog.update_emote_usage_statistics.start()
                log_info("Emote usage statistics update task started.")
            else:
                log_error("UpdateEmoteUsageTask cog not found.")
        except Exception as e:
            log_error(f"Error starting the scheduled task: {e}", exc_info=True)


async def setup(bot):
    await bot.add_cog(StartScheduledTask(bot))
