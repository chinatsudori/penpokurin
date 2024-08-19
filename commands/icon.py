import discord
from discord.ext import commands
from helpers.google_sheets import get_gspread_client
from helpers.error_handler import GoogleSheetsAPIError, send_log_message

class IconCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = get_gspread_client()
        self.sheet = self.client

    @commands.command()
    async def icon(self, ctx, *, unit_name: str = None):
        if unit_name is None:
            # Display the current server icon
            embed = discord.Embed(
                title="Current Icon",
                description=f"Here is the current icon: {ctx.guild.icon_url}",
                color=discord.Color.blue(),
            )
            await ctx.send(embed=embed)
            await send_log_message(f"{ctx.author} requested the current server icon.")
        else:
            # Fetch the unit icon from Google Sheets
            unit_icons_sheet = self.sheet.worksheet("Unit Icons")
            try:
                cell = unit_icons_sheet.find(unit_name, in_column=10)
                if cell:
                    icon_url = unit_icons_sheet.cell(cell.row, 8).value
                    embed = discord.Embed(
                        title=f"Icon for '{unit_name}'",
                        description=f"[Click here to view the icon]({icon_url})",
                        color=discord.Color.blue(),
                    )
                    await ctx.send(embed=embed)
                    await send_log_message(f"Icon for '{unit_name}' requested by {ctx.author}.")
                else:
                    embed = discord.Embed(
                        title="Unit Not Found",
                        description=f"The unit name '{unit_name}' was not found in the Unit Icons sheet.",
                        color=discord.Color.red(),
                    )
                    await ctx.send(embed=embed)
                    await send_log_message(f"Unit '{unit_name}' not found when requested by {ctx.author}.")
            except GoogleSheetsAPIError as e:
                await ctx.send(embed=e.error_embed)
                await send_log_message(f"Google Sheets API Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                await send_log_message(f"Unexpected Error: {e}")

async def setup(bot):
    await bot.add_cog(IconCommand(bot))
