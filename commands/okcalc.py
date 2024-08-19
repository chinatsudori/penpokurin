import discord
from discord.ext import commands

class OkcalcCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def okcalc(self, ctx, *args):
        if len(args) == 3:
            # Complex boss calculation
            try:
                boss_hp, dmg_a, dmg_b = map(int, args)

                def calculate_results(boss_hp, dmg_a, dmg_b):
                    if dmg_a + dmg_b <= boss_hp:
                        return "*打不死*", 0
                    if boss_hp - dmg_a <= 0:
                        return "*一刀秒了*", boss_hp - dmg_a
                    seconds_a = min(90, round(110 - (boss_hp - dmg_a) / dmg_b * 90))
                    points_a = (
                        boss_hp - dmg_a
                        if boss_hp - dmg_a <= 0
                        else round((boss_hp - dmg_a) - (90 - seconds_a) / 90 * dmg_b)
                    )

                    if boss_hp - dmg_b <= 0:
                        return "*一刀秒了*", boss_hp - dmg_b
                    seconds_b = min(90, round(110 - (boss_hp - dmg_b) / dmg_a * 90))
                    points_b = (
                        boss_hp - dmg_b
                        if boss_hp - dmg_b <= 0
                        else round((boss_hp - dmg_b) - (90 - seconds_b) / 90 * dmg_a)
                    )

                    return (seconds_a, points_a), (seconds_b, points_b)

                result_a, result_b = calculate_results(boss_hp, dmg_a, dmg_b)

                embed = discord.Embed(
                    title="OK Calc Results", color=discord.Color.blue()
                )

                if result_a == "*打不死*":
                    embed.add_field(
                        name="A Finishes First", value="打不死", inline=False
                    )
                elif result_a == "*一刀秒了*":
                    embed.add_field(
                        name="A Finishes First", value="一刀秒了", inline=False
                    )
                else:
                    seconds_a, points_a = result_a
                    embed.add_field(
                        name="A Finishes First",
                        value=f"B receives {seconds_a:,} seconds and {points_a:,} dmg score",
                        inline=False,
                    )

                if result_b == "*打不死*":
                    embed.add_field(
                        name="B Finishes First", value="打不死", inline=False
                    )
                elif result_b == "*一刀秒了*":
                    embed.add_field(
                        name="B Finishes First", value="一刀秒了", inline=False
                    )
                else:
                    seconds_b, points_b = result_b
                    embed.add_field(
                        name="B Finishes First",
                        value=f"A receives {seconds_b:,} seconds and {points_b:,} dmg score",
                        inline=False,
                    )

                await ctx.send(embed=embed)

            except ValueError:
                embed = discord.Embed(
                    title="Error",
                    description="Invalid input. Please provide three integers for boss HP, dmg A, and dmg B.",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title="Error",
                    description=f"An error occurred: {e}",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="Invalid number of arguments. Provide three integers for boss calculation.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(OkcalcCommand(bot))
