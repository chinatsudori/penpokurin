import discord
from discord.ext import commands
from helpers.google_sheets import get_gspread_client, get_player_name
from helpers.error_handler import GoogleSheetsAPIError, send_log_message

class IDCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = get_gspread_client()
        self.sheet = self.client

    @commands.command()
    async def id(self, ctx):
        user_id = str(ctx.author.id)
        print(f"Received ID command from {ctx.author.name} ({user_id})")  # Debug print

        try:
            player_name = get_player_name(user_id)
            if not player_name:
                embed = discord.Embed(
                    title="No Player Name Assigned",
                    description="You have not assigned a player name. Use `!iam <player_name>` first.",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
                await send_log_message(f"{ctx.author} attempted to use the `!id` command without an assigned player name.")
                return

            friend_ids_sheet = self.sheet.worksheet("Friend IDs")
            print(f"Searching for player name: {player_name}")  # Debug print
            player_cell = friend_ids_sheet.find(player_name, in_column=2)
            if player_cell:
                print(f"Player name found at row {player_cell.row}")  # Debug print
                friend_id = friend_ids_sheet.cell(player_cell.row, 3).value
                embed = discord.Embed(
                    title=f"The friend ID for '{player_name}' is:",
                    description=f"{friend_id}",
                    color=discord.Color.blue(),
                )
                await ctx.send(embed=embed)
                await send_log_message(f"{ctx.author} retrieved friend ID for '{player_name}'.")
            else:
                embed = discord.Embed(
                    title="Player Name Not Found",
                    description=f"Player name '{player_name}' not found in the Friend IDs sheet.",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
                await send_log_message(f"{ctx.author} searched for '{player_name}' but it was not found.")
        except GoogleSheetsAPIError as e:
            await ctx.send(embed=e.error_embed)
            await send_log_message(f"Google Sheets API Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            await send_log_message(f"Unexpected Error: {e}")

async def setup(bot):
    await bot.add_cog(IDCommand(bot))
