import discord
from discord.ext import commands
from helpers.google_sheets import get_gspread_client, get_high_priority_support_units
from helpers.error_handler import GoogleSheetsAPIError

# Assuming get_gspread_client, get_high_priority_support_units, and GoogleSheetsAPIError are defined elsewhere

class HipriCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = get_gspread_client()
        self.sheet = self.client.open("Your Spreadsheet Name").sheet1  # Assuming you're working with the first sheet

    async def send_log_message(self, message):
        # Log the message to a specific channel or console
        log_channel = discord.utils.get(self.bot.get_all_channels(), name="log-channel")
        if log_channel:
            await log_channel.send(message)
        else:
            print(message)  # Fallback to console logging

    @commands.command()
    async def hipri(self, ctx, *, message: str = None):
        if message:
            channel = discord.utils.get(ctx.guild.text_channels, name="high-priority")
            if channel:
                embed = discord.Embed(
                    title="High Priority",
                    description=message,
                    color=discord.Color.red(),
                )
                await channel.send(embed=embed)
                await self.send_log_message(f"High-priority message sent by {ctx.author}: {message}")
            else:
                embed = discord.Embed(
                    title="Error",
                    description="The 'high-priority' channel was not found.",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
                await self.send_log_message(f"Error: 'high-priority' channel not found for {ctx.author}")
        else:
            try:
                zero_set_names = get_high_priority_support_units(self.sheet)
                if zero_set_names:
                    formatted_names = [f"- {name}" for name in zero_set_names]
                    embed = discord.Embed(
                        title="Needed High Priority Support Units",
                        description=(
                            "After setting your support, type '!support cb [1 or 2] [name] [UE Level] [notes]' into chat.\n\n"
                            "Please consider setting one of the following units:\n"
                            + "\n".join(formatted_names)
                        ),
                        color=discord.Color.blue(),
                    )
                else:
                    embed = discord.Embed(
                        title="No High Priority Units Missing",
                        description="No high priority units are currently missing.",
                        color=discord.Color.green(),
                    )
                await ctx.send(embed=embed)
            except GoogleSheetsAPIError as e:
                await ctx.send(embed=e.error_embed)
                await self.send_log_message(f"Google Sheets API Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                embed = discord.Embed(
                    title="Error",
                    description="An unexpected error occurred. Please try again later.",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
                await self.send_log_message(f"An unexpected error occurred: {e}")
async def setup(bot):
    await bot.add_cog(HipriCommand(bot))
