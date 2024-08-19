import discord
from discord.ext import commands


class ToolsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tools(self, ctx):
        tools_list = [
            {
                "name": "Origami Tools",
                "url": "https://docs.google.com/spreadsheets/d/1n2aGPJ41QOUsHn0pzF7kFl-TZdJD_h59-tXZDBQLkEY/edit?gid=1232445958#gid=1232445958",
            }
        ]

        embed = discord.Embed(
            title="Tools",
            description="Here are some useful tools:",
            color=discord.Color.blue(),
        )

        for tool in tools_list:
            embed.add_field(name=tool["name"], value=tool["url"], inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ToolsCommand(bot))
