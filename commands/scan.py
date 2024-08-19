from discord.ext import commands
from helpers.google_sheets import store_emote_usage_statistics
from helpers.emote_utils import fetch_chat_messages, extract_emote_usage

class EmoteUsageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='scan_emotes')
    async def scan_emotes(self, ctx):
        channel_id = 1102558718937288717
        channel = self.bot.get_channel(channel_id)

        if not channel:
            await ctx.send("Channel not found.")
            return

        try:
            # Fetch the last 137,000 messages
            messages = await fetch_chat_messages([channel], limit=137000)
            emote_usage = extract_emote_usage(messages)

            # Store the emote usage in Google Sheets or another desired location
            store_emote_usage_statistics(emote_usage)

            await ctx.send(f"Emote usage statistics have been tallied for {len(messages)} messages.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")


async def setup(bot):
    await bot.add_cog(EmoteUsageCommands(bot))
