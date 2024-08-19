import discord
from discord.ext import commands
import random
from helpers.error_handler import send_log_message

class CommandErrorEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(f"An error occurred with the command '{ctx.command}': {error}")  # Debug print

        # Log the error message
        error_message = (
            f"An error occurred with the command '{ctx.command}': {error}"
        )
        await send_log_message(error_message)

        if isinstance(error, commands.CommandNotFound):
            responses = [
                "Dururururu~",
                "Nyaanya~",
                "Pyon pyon pyoon~",
                "Kira kira~",
                "Mofu mofu~",
                "Uauuuuuu~",
                "Wan wan~",
                "kyuuuuuun~",
                "*Angrykotsounds*",
            ]
            response = random.choice(responses)
            embed = discord.Embed(
                title="bzzzzt~", description=response, color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CommandErrorEvents(bot))
