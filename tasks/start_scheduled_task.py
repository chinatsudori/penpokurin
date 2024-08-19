from discord.ext import commands, tasks
import asyncio
from helpers.time_utils import get_current_time, get_start_of_next_day
from .update_emote_usage import UpdateEmoteUsageTask
from helpers.error_handler import send_log_message


class StartScheduledTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_scheduled_task.start()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.start_scheduled_task()

    @tasks.loop(hours=24)  # Run every 24 hours
    async def start_scheduled_task(self):
        now = await get_current_time()
        next_run = await get_start_of_next_day()
        delay = (next_run - now).total_seconds()
        await asyncio.sleep(delay)
        self.bot.get_cog(UpdateEmoteUsageTask).update_emote_usage_statistics.start()
 
 

async def setup(bot):
    await bot.add_cog(StartScheduledTask(bot))
