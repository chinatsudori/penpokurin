from discord.ext import tasks, commands
from config import EMOTE_CHAN
from helpers.google_sheets import store_emote_usage_statistics
from helpers.emote_utils import fetch_chat_messages, extract_emote_usage
from lib.error_handler import log_info, log_error  # Update the import path


class UpdateEmoteUsageTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_emote_usage_statistics.start()

    def cog_unload(self):
        self.update_emote_usage_statistics.cancel()

    @tasks.loop(hours=24)  # Run every 24 hours
    async def update_emote_usage_statistics(self):
        try:
            channels = [self.bot.get_channel(channel_id) for channel_id in EMOTE_CHAN]
            missing_channels = [
                channel_id
                for channel_id, channel in zip(EMOTE_CHAN, channels)
                if channel is None
            ]
            if missing_channels:
                log_error(f"One or more channels not found: {missing_channels}.")
                return

            messages = await fetch_chat_messages(channels)
            emote_usage = extract_emote_usage(messages)
            try:
                store_emote_usage_statistics(emote_usage)
            except Exception as e:
                log_error(f"Failed to store emote usage statistics: {e}", exc_info=True)
                return

            log_info("Emote usage statistics updated successfully.")
        except Exception as e:
            log_error(
                f"An error occurred while updating emote usage statistics: {e}",
                exc_info=True,
            )

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.update_emote_usage_statistics.is_running():
            self.update_emote_usage_statistics.start()


async def setup(bot):
    await bot.add_cog(UpdateEmoteUsageTask(bot))
