from discord.ext import tasks, commands
from config import EMOTE_CHAN
from helpers.google_sheets import store_emote_usage_statistics
from helpers.emote_utils import fetch_chat_messages, extract_emote_usage
from helpers.error_handler import send_log_message

class UpdateEmoteUsageTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_emote_usage_statistics.start()

    @tasks.loop(hours=24)  # Run every 24 hours
    async def update_emote_usage_statistics(self):
        try:
            channels = [self.bot.get_channel(channel_id) for channel_id in EMOTE_CHAN]
            if not all(channels):
                await send_log_message(self.bot, "Emote Channel Error", "One or more channels not found.", discord.Color.red())
                return

            messages = await fetch_chat_messages(channels)
            emote_usage = extract_emote_usage(messages)
            store_emote_usage_statistics(emote_usage)

            await send_log_message(self.bot, "Emote Usage Update", "Emote usage statistics updated successfully.", discord.Color.green())
        except Exception as e:
            await send_log_message(self.bot, "Emote Usage Update Error", f"An error occurred while updating emote usage statistics: {e}", discord.Color.red())

async def setup(bot):
    await bot.add_cog(UpdateEmoteUsageTask(bot))
