import discord
from discord.ext import commands


class HitPlannerCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hitplanner(self, ctx):
        # Create an embed message
        embed = discord.Embed(
            title="Hit Planner Guide",
            description="Here's a short guide on using the hit planner website for CB. Check it out and see if it makes CB easier for you!",
            color=discord.Color.blue(),
        )

        # Add fields to the embed
        embed.add_field(name="Step 1", value="Go to the Options page", inline=False)
        embed.add_field(
            name="Step 2",
            value="Under Available Units, deselect all the units you don't own/don't have built",
            inline=False,
        )
        embed.add_field(
            name="Step 3",
            value="Go back to the planner page and select your desired bosses",
            inline=False,
        )
        embed.add_field(
            name="Step 4",
            value='Use the Desired Timings section to filter what type of comp you want to use. "video" and "manual" will usually involve a more complex TL, "semi auto" will be found in the Worrychefs sheet, and "full auto" is self-explanatory.',
            inline=False,
        )
        embed.add_field(
            name="Step 5",
            value='Press "score pad" and the planner will automatically select the 3 highest scoring teams for you according to your box and selected bosses. Most of the time, you\'ll want to avoid hitting the same boss twice in Tier 4. Exception is when the boss is very unpopular and needs more hits to take down.',
            inline=False,
        )
        embed.add_field(
            name="Step 6",
            value="To save your unit selections, copy the link under Available Units in the Options page.",
            inline=False,
        )

        # Add the hit planner link
        embed.add_field(
            name="Hit Planner Link",
            value="[Click here](https://s3-us-west-2.amazonaws.com/holatuwol/priconne/cb77.html)",
            inline=False,
        )

        # Set the footer
        embed.set_footer(text="Pyon Pyon Pyooon~")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HitPlannerCommand(bot))
