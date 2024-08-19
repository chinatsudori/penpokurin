import discord
import asyncio
from discord.ext import tasks, commands
from config import CHANNEL_ID, CLAN_ROLE_ID
from helpers.time_utils import get_current_time, get_time_difference, add_hours_to_time
from helpers.google_sheets import get_scheduled_time
from lib.error_handler import (
    log_info,
    log_error,
    log_debug,
)  # Import logging functions


class ScheduledMessageTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log_debug("ScheduledMessageTask cog initialized.")
        self.scheduled_message.start()

    @tasks.loop(minutes=1)  # Check every minute
    async def scheduled_message(self):
        try:
            now = await get_current_time()
            log_debug(f"Current time: {now}")

            scheduled_time = get_scheduled_time()
            log_debug(f"Scheduled message time: {scheduled_time}")

            if now >= scheduled_time:
                channel = self.bot.get_channel(CHANNEL_ID)
                if channel:
                    embed = discord.Embed(
                        title="Reminder for this CB",
                        description=(
                            f"<@&{CLAN_ROLE_ID}>\n\n"
                            "We use this spreadsheet to track CB attempts. If possible, please try to fill in your own attempts after completing them.\n\n"
                            "We also use it as a guide for what to set our CB support units as, and an accurate summary of what units are currently set as support by everyone. Please check the High Priority Support list in the spreadsheet and set your support units in the Master Sheet.\n\n"
                            "Try to hit tier 4, but use tier down if a tier 4 boss is too difficult for you to hit effectively.\n"
                            "If using tier down to hit tier 3, try to spend all of your attempts including carryover on C5.\n\n"
                            "Check the comps and the individual tier channels for comps to use in CB, and request any support units you need in <#1221944116926222377> (feel free to ping the <@&{CLAN_ROLE_ID}> role).\n\n"
                            "https://docs.google.com/spreadsheets/d/1n2aGPJ41QOUsHn0pzF7kFl-TZdJD_h59-tXZDBQLkEY/edit?usp=sharing"
                        ),
                        color=discord.Color.blue(),
                    )
                    await channel.send(embed=embed)
                    log_info("Scheduled message sent to the channel.")

                self.scheduled_message.cancel()
                log_debug("Scheduled message task canceled after sending the message.")
        except Exception as e:
            log_error(
                f"An error occurred in the scheduled message task: {e}", exc_info=True
            )


async def schedule_follow_up_messages(self, channel, scheduled_time):
    try:
        times = [23, 47, 71, 95, 96]  # in hours

        for hours in times:
            target_time = add_hours_to_time(scheduled_time, hours)
            log_debug(f"Scheduled follow-up message at: {target_time} (hours: {hours})")

            sleep_duration = get_time_difference(get_current_time(), target_time)
            if sleep_duration > 0:
                await asyncio.sleep(sleep_duration)
            else:
                log_info("Target time already passed. Skipping sleep.")

            if hours < 96:
                embed = discord.Embed(
                    title="Reminder",
                    description=f"<@&{CLAN_ROLE_ID}> One hour left until reset.",
                    color=discord.Color.orange(),
                )
            else:
                end_time = add_hours_to_time(target_time, 19)
                embed = discord.Embed(
                    title="Final Reminder",
                    description=(
                        f"<@&{CLAN_ROLE_ID}> Reminder that CB ends earlier today "
                        f"(in <t:{int(end_time.timestamp())}:R>). Make sure not to miss hits due to CB ending unexpectedly."
                    ),
                    color=discord.Color.red(),
                )

            await channel.send(embed=embed)
            log_info(f"Follow-up message sent: {embed.title}")
    except Exception as e:
        log_error(
            f"An error occurred while scheduling follow-up messages: {e}", exc_info=True
        )


async def setup(bot):
    await bot.add_cog(ScheduledMessageTask(bot))
