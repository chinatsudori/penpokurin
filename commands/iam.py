import discord
from discord.ext import commands
from helpers.google_sheets import get_gspread_client
from helpers.error_handler import GoogleSheetsAPIError, send_log_message

class IAMCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = get_gspread_client()
        self.sheet = self.client

    @commands.command()
    async def iam(self, ctx, *, player_name: str):
        user_id = str(ctx.author.id)
        try:
            friend_ids_sheet = self.sheet.worksheet("Friend IDs")

            log_message = f"Searching for player name: {player_name}"
            print(log_message)
            await send_log_message(log_message)

            cell = friend_ids_sheet.find(player_name, in_column=2)
            if cell:
                log_message = f"Player name found at row {cell.row}"
                print(log_message)
                await send_log_message(log_message)

                discord_id_cell = friend_ids_sheet.cell(cell.row, 4).value
                if discord_id_cell:
                    embed = discord.Embed(
                        title="Player Name Already Taken",
                        description=f"The player name '{player_name}' is already taken.",
                        color=discord.Color.red(),
                    )
                    await ctx.send(embed=embed)
                    await send_log_message(f"Player name '{player_name}' is already taken by another user.")
                else:
                    friend_ids_sheet.update_cell(cell.row, 4, user_id)
                    embed = discord.Embed(
                        title="Player Name Assigned",
                        description=f"{ctx.author.mention}, you have been assigned the player name '{player_name}'.",
                        color=discord.Color.green(),
                    )
                    await ctx.send(embed=embed)
                    await send_log_message(f"{ctx.author} has been assigned the player name '{player_name}'.")
            else:
                embed = discord.Embed(
                    title="Player Name Not Found",
                    description=f"The player name '{player_name}' was not found in the list.",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
                await send_log_message(f"Player name '{player_name}' was not found in the list.")
        except GoogleSheetsAPIError as e:
            await ctx.send(embed=e.error_embed)
            await send_log_message(f"Google Sheets API Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            await send_log_message(f"Unexpected Error: {e}")

async def setup(bot):
    await bot.add_cog(IAMCommand(bot))
