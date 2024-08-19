import discord
from discord.ext import commands
from helpers.google_sheets import (
    get_gspread_client,
    get_current_month_sheet,
    get_player_name,
)
from helpers.error_handler import GoogleSheetsAPIError, send_log_message
class CBCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = get_gspread_client()
        self.sheet = self.client

    @commands.command()
    async def cb(self, ctx, action: str, day: int = None, attempt: int = None):
        user_id = str(ctx.author.id)
        friend_ids_sheet = self.sheet.worksheet("Friend IDs")

        try:
            # Check if the user has assigned a player name
            discord_id_cells = friend_ids_sheet.findall(user_id, in_column=4)
            if not discord_id_cells:
                embed = discord.Embed(
                    title="Player Name Required",
                    description="You have not assigned a player name. Use `!iam <player_name>` first.",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
                return

            # Get the player name associated with the user
            player_row = discord_id_cells[0].row
            player_name = friend_ids_sheet.cell(player_row, 2).value

            # Access the current month's sheet
            month_sheet = get_current_month_sheet()

            # Find the player's row in the month's sheet
            player_cell = month_sheet.find(player_name, in_column=1)
            if not player_cell:
                embed = discord.Embed(
                    title="Player Name Not Found",
                    description=f"Player name '{player_name}' not found in the current month's sheet.",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
                return

            player_row = player_cell.row

            if action.lower() == "tick":
                if day and attempt:
                    # Validate day and attempt numbers
                    if day < 1 or day > 5 or attempt < 1 or attempt > 3:
                        embed = discord.Embed(
                            title="Invalid Input",
                            description="Invalid day or attempt number. Days: 1-5, Attempts: 1-3.",
                            color=discord.Color.red(),
                        )
                        await ctx.send(embed=embed)
                        return
                    column = 2 + (day - 1) * 3 + (attempt - 1)
                    message = f"{player_name}'s checkbox for day {day}, attempt {attempt} has been ticked."
                else:
                    # Find the first empty checkbox for this player
                    column = 2
                    while month_sheet.cell(player_row, column).value and column <= 17:
                        column += 3
                    if column > 17:
                        embed = discord.Embed(
                            title="No Empty Checkboxes",
                            description=f"All checkboxes for {player_name} are filled.",
                            color=discord.Color.red(),
                        )
                        await ctx.send(embed=embed)
                        return
                    message = f"{player_name}'s first empty checkbox has been ticked."

                # Update the sheet
                month_sheet.update_cell(player_row, column, "X")

                # Send confirmation message
                embed = discord.Embed(
                    title="Checkbox Ticked",
                    description=message,
                    color=discord.Color.green(),
                )
                await ctx.send(embed=embed)

            elif action.lower() == "untick":
                if day and attempt:
                    # Validate day and attempt numbers
                    if day < 1 or day > 5 or attempt < 1 or attempt > 3:
                        embed = discord.Embed(
                            title="Invalid Input",
                            description="Invalid day or attempt number. Days: 1-5, Attempts: 1-3.",
                            color=discord.Color.red(),
                        )
                        await ctx.send(embed=embed)
                        return
                    column = 2 + (day - 1) * 3 + (attempt - 1)
                    message = f"{player_name}'s checkbox for day {day}, attempt {attempt} has been reset."
                else:
                    # Find the first filled checkbox for this player
                    column = 2
                    while (
                        month_sheet.cell(player_row, column).value != "X"
                        and column <= 17
                    ):
                        column += 3
                    if column > 17:
                        embed = discord.Embed(
                            title="No Filled Checkboxes",
                            description=f"No checkboxes are ticked for {player_name}.",
                            color=discord.Color.red(),
                        )
                        await ctx.send(embed=embed)
                        return
                    message = f"{player_name}'s first filled checkbox has been reset."

                # Update the sheet
                month_sheet.update_cell(player_row, column, "")

                # Send confirmation message
                embed = discord.Embed(
                    title="Checkbox Reset",
                    description=message,
                    color=discord.Color.green(),
                )
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(
                    title="Invalid Action",
                    description="Invalid action. Use 'tick' or 'reset'.",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)

        except GoogleSheetsAPIError as e:
            await ctx.send(embed=e.error_embed)
            await send_log_message(f"GoogleSheetsAPIError: {e}")

        except Exception as e:
            await ctx.send(embed=discord.Embed(
                title="Unexpected Error",
                description=f"An unexpected error occurred: {e}",
                color=discord.Color.red(),
            ))
            await send_log_message(f"Unexpected error in cb command: {e}")

async def setup(bot):
    await bot.add_cog(CBCommand(bot))
