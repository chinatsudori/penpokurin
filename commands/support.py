import discord
from discord.ext import commands
from helpers.google_sheets import (
    get_gspread_client,
    get_player_name,
    validate_unit_name,
)
from helpers.error_handler import GoogleSheetsAPIError, send_log_message
from helpers.time_utils import get_current_utc_time

class SupportCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = get_gspread_client()
        self.sheet = self.client

    @commands.command()
    async def support(
        self, ctx, cb_or_quest: str, pos: int, name: str, ue: str, *, note: str
    ):
        user_id = str(ctx.author.id)
        player_name = get_player_name(user_id)
        if not player_name:
            embed = discord.Embed(
                title="Player Name Required",
                description="You have not assigned a player name. Use `!iam <player_name>` first.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            await send_log_message(f"{ctx.author} tried to set support but has no assigned player name.")
            return

        # Determine the correct column based on CB/Quest and position
        if cb_or_quest.lower() == "cb":
            if pos == 1:
                col = 2  # Column B
            elif pos == 2:
                col = 3  # Column C
            else:
                embed = discord.Embed(
                    title="Invalid Position",
                    description="Invalid position for CB. Use `1` or `2`.",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
                await send_log_message(f"{ctx.author} used an invalid position for CB: {pos}.")
                return
        elif cb_or_quest.lower() == "quest":
            if pos == 1:
                col = 5  # Column E
            elif pos == 2:
                col = 6  # Column F
            else:
                embed = discord.Embed(
                    title="Invalid Position",
                    description="Invalid position for Quest. Use `1` or `2`.",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
                await send_log_message(f"{ctx.author} used an invalid position for Quest: {pos}.")
                return
        else:
            embed = discord.Embed(
                title="Invalid Type",
                description="Invalid type. Use `CB` or `Quest`.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            await send_log_message(f"{ctx.author} used an invalid type: {cb_or_quest}.")
            return

        # Validate unit name
        if not validate_unit_name(name):
            embed = discord.Embed(
                title="Invalid Unit Name",
                description=f"The unit name '{name}' is not found in the Character List.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            await send_log_message(f"{ctx.author} provided an invalid unit name: {name}.")
            return

        # Update the Support sheet
        try:
            support_sheet = self.sheet.worksheet("Support")
            player_cell = support_sheet.find(player_name, in_column=1)
            if not player_cell:
                embed = discord.Embed(
                    title="Player Name Not Found",
                    description=f"Player name '{player_name}' not found in the Support sheet.",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
                await send_log_message(f"{ctx.author}'s player name '{player_name}' not found in Support sheet.")
                return

            player_row = player_cell.row
            current_time = get_current_utc_time()
            support_sheet.update_cell(player_row, col, name)
            support_sheet.update_cell(player_row, col + 1, ue)
            support_sheet.update_cell(player_row, col + 2, note)
            support_sheet.update_cell(player_row, 8, current_time)

            embed = discord.Embed(
                title="Support Set",
                description=f"{ctx.author.mention}, your support info for {cb_or_quest} position {pos} has been set.",
                color=discord.Color.green(),
            )
            await ctx.send(embed=embed)
            await send_log_message(f"{ctx.author} set support for {cb_or_quest} position {pos} with unit '{name}', UE '{ue}', note '{note}'.")
        except GoogleSheetsAPIError as e:
            await ctx.send(embed=e.error_embed)
            await send_log_message(f"Google Sheets API Error: {e}")

async def setup(bot):
    await bot.add_cog(SupportCommand(bot))
