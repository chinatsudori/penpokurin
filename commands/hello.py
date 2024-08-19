import discord
from discord.ext import commands

class HelloCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        embed = discord.Embed(
            title="Bzzzt~",
            description=f"Hello, {ctx.author.mention}!",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelloCommand(bot))
