from discord.ext import commands
from helpers.google_sheets import (
    get_gspread_client,
    get_player_name,
    get_current_month_sheet,
)
from helpers.time_utils import (
    calculate_cb_number,
    parse_date,
    add_days_to_date,
    format_date,
    get_next_month_date,
)
from helpers.error_handler import GoogleSheetsAPIError, send_log_message
import discord


class SetCBCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
<<<<<<< HEAD
        self.client = get_gspread_client()
        self.sheet = self.client.open(SHEET)  # Correctly open the spreadsheet here
=======
        self.sheet = get_gspread_client()  # Assign the Spreadsheet object to self.sheet
>>>>>>> parent of bb100f4 (cb sheet)

    @commands.command()
    async def setcb(self, ctx, date_str: str = None):
        user_id = str(ctx.author.id)
        player_name = get_player_name(user_id)
        if not player_name:
            embed = discord.Embed(
                title="Player Name Required",
                description="You have not assigned a player name. Use `!iam <player_name>` first.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            await send_log_message(f"{ctx.author} tried to set CB without an assigned player name.")
            return

        current_cb_number = calculate_cb_number()
        current_sheet_name = get_current_month_sheet().title

        if f"CB{current_cb_number:02d}" in current_sheet_name:
            embed = discord.Embed(
                title="Clan Battle Already Set",
                description=f"The current Clan Battle month is already set to CB{current_cb_number:02d}. No changes were made.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            await send_log_message(f"{ctx.author} attempted to set CB but it was already set to CB{current_cb_number:02d}.")
            return

        if date_str:
            try:
                start_date = parse_date(date_str)
                end_date = add_days_to_date(start_date, 5)
                start_date_str = format_date(start_date)
                end_date_str = format_date(end_date)

                ppkn_sheet = self.sheet.worksheet(
                    "ppkn"
                )  # Use worksheet method on the Spreadsheet object
                ppkn_sheet.update("B1", [[start_date_str]])
                ppkn_sheet.update("C1", [[end_date_str]])

                next_month_name = start_date.strftime("%B")
                next_sheet_name = f"{next_month_name} CB (CB{current_cb_number:02d})"

                range_to_clear = "B5:P34"
                num_rows = 30
                num_cols = ord("P") - ord("B") + 1
                clear_values = [[False] * num_cols for _ in range(num_rows)]
                current_sheet = get_current_month_sheet()
                current_sheet.update(range_to_clear, clear_values)
                current_sheet.update_title(next_sheet_name)

                embed = discord.Embed(
                    title="CB Dates Set and Sheet Updated",
                    description=(
                        f"CB start date set to {start_date_str}.\n"
                        f"CB end date set to {end_date_str}.\n"
                        f"Renamed the current sheet to '{next_sheet_name}' and cleared checkboxes in B5:P34."
                    ),
                    color=discord.Color.green(),
                )
                await ctx.send(embed=embed)
                await send_log_message(f"{ctx.author} set CB dates to {start_date_str} - {end_date_str} and updated the sheet.")
            except ValueError:
                embed = discord.Embed(
                    title="Invalid Date Format",
                    description="Invalid date format. Please use mm/dd.",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
                await send_log_message(f"{ctx.author} used an invalid date format: {date_str}.")
            except GoogleSheetsAPIError as e:
                await ctx.send(embed=e.error_embed)
                await send_log_message(f"Google Sheets API Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                embed = discord.Embed(
                    title="Unexpected Error",
                    description="An unexpected error occurred. Please try again later.",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
                await send_log_message(f"Unexpected Error: {e}")
        else:
            try:
                current_month_sheet = get_current_month_sheet()
                archive_sheet = self.sheet.worksheet(
                    "Archive"
                )  # Use worksheet method on the Spreadsheet object

                archive_sheet.clear()
                current_month_data = current_month_sheet.get_all_values()
                archive_sheet.update("A1", current_month_data)

                current_month_sheet.clear()
                new_month_data = self.sheet.worksheet(
                    get_next_month_date().strftime("%B")
                ).get_all_values()
                current_month_sheet.update("A1", new_month_data)

                embed = discord.Embed(
                    title="Clan Battle Set",
                    description=f"The current Clan Battle month has been set to CB{current_cb_number}.",
                    color=discord.Color.green(),
                )
                await ctx.send(embed=embed)
                await send_log_message(f"{ctx.author} set the Clan Battle month to CB{current_cb_number}.")
            except GoogleSheetsAPIError as e:
                await ctx.send(embed=e.error_embed)
                await send_log_message(f"Google Sheets API Error: {e}")

async def setup(bot):
    await bot.add_cog(SetCBCommand(bot))
