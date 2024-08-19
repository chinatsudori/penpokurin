from discord import Embed
from discord.ext import commands
import asyncio

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx, command_name: str = None):
        if command_name == "cal":
            embed = Embed(
                title="Command Help: !cal",
                description="Learn how to use the `!cal` command to create or update events using a JSON string.",
                color=0x00FF00,
            )
            embed.add_field(name="Usage", value="`!cal <json>`", inline=False)
            embed.add_field(
                name="Details",
                value=(
                    "Parses the provided JSON string containing event details and creates or updates "
                    "scheduled events in the server using Carl-bot. The JSON string should follow the format "
                    "expected by the bot, listing all events to be processed."
                ),
                inline=False,
            )
            embed.set_footer(
                text="Make sure your JSON is properly formatted to avoid errors."
            )
            await ctx.send(embed=embed)

        elif command_name == "cb":
            embed = Embed(
                title="Command Help: !cb",
                description="Manage your Clan Battle attempts with the `!cb` command.",
                color=0x00FF00,
            )
            embed.add_field(
                name="Usage", value="`!cb <action> [day] [attempt]`", inline=False
            )
            embed.add_field(
                name="Arguments",
                value=(
                    "**action**: 'tick' to mark an attempt or 'untick' to reset a marked attempt.\n"
                    "**day**: The day of the battle (1-5). This is optional for 'tick'.\n"
                    "**attempt**: The attempt number for that day (1-3). This is optional for 'tick'.\n"
                    "If you don't specify day and attempt, the first empty slot will be ticked. You must specify both for 'untick'."
                ),
                inline=False,
            )
            embed.add_field(
                name="Examples",
                value=(
                    "`!cb tick 3 2` - Marks the second attempt on the third day.\n"
                    "`!cb untick 2 1` - Resets the first attempt on the second day.\n"
                    "`!cb tick` - Marks the first empty slot available."
                ),
                inline=False,
            )
            embed.set_footer(
                text="Ensure your player name is assigned with `!iam <player_name>` before using this command."
            )
            await ctx.send(embed=embed)

        elif command_name == "iam":
            embed = Embed(
                title="Command Help: !iam",
                description="Set your player name to sync with your Discord name.",
                color=0x00FF00,
            )
            embed.add_field(name="Usage", value="`!iam <player_name>`", inline=False)
            embed.add_field(
                name="Arguments",
                value=(
                    "**name**: Specify your in-game player name to sync with your Discord name.\n"
                ),
                inline=False,
            )
            embed.add_field(
                name="Examples",
                value=(
                    "`!iam Theaceae` - Sets your player name to Theaceae.\n"
                    "**NOTE** You cannot use a player name that has already been claimed by another Discord ID. Contact a Clan Manager if you think this is an error.\n"
                ),
                inline=False,
            )
            embed.set_footer(
                text="This command is **REQUIRED** before running most commands."
            )
            await ctx.send(embed=embed)

        elif command_name == "okcalc":
            embed = Embed(
                title="Command Help: !okcalc",
                description="Calculate overkill damage sharing with the `!okcalc` command.",
                color=0x00FF00,
            )
            embed.add_field(
                name="Usage",
                value="`!okcalc <remaining_boss_hp> <player_a_damage> <player_b_damage>`",
                inline=False,
            )
            embed.add_field(
                name="Arguments",
                value=(
                    "**remaining_boss_hp**: The HP left on the boss.\n"
                    "**player_a_damage**: The damage Player A will do.\n"
                    "**player_b_damage**: The damage Player B will do."
                ),
                inline=False,
            )
            embed.add_field(
                name="Examples",
                value=(
                    "`!okcalc 100000 90000 150000` - Calculates how Player A and Player B should split the overkill damage."
                ),
                inline=False,
            )
            embed.set_footer(
                text="Use this command to optimize your Clan Battle overkill damage sharing."
            )
            await ctx.send(embed=embed)

        elif command_name == "support":
            embed = Embed(
                title="Command Help: !support",
                description="Register your support units for Clan Battle or quests using the !support command.",
                color=0x00FF00,
            )
            embed.add_field(
                name="Usage",
                value="!support <support type> <position> <name of unit> <UE level of unit> [note]",
                inline=False,
            )
            embed.add_field(
                name="Arguments",
                value=(
                    "**support type**: Specify 'cb' for Clan Battle or 'quest' for quests.\n"
                    "**position**: The position number (1 or 2) for the support unit.\n"
                    "**name of unit**: The name of the support unit.\n"
                    "**UE level of unit**: The unit's UE level.\n"
                    "**note**: (Optional) Any additional notes about the unit (e.g., LB, 6*, etc).\n"
                ),
                inline=False,
            )
            embed.add_field(
                name="Examples",
                value=(
                    "!support cb 1 Hero 6* LB - Registers Hero in position 1 for Clan Battle with UE level 6* and a note LB.\n"
                    "!support quest 2 Ranger 5* - Registers Ranger in position 2 for a quest with UE level 5*.\n"
                ),
                inline=False,
            )
            embed.set_footer(
                text="Ensure all details are accurate to avoid any confusion."
            )
            await ctx.send(embed=embed)

        else:
            message = await ctx.send(embed=self.help_pages[0])
            await message.add_reaction('⬅️')
            await message.add_reaction('➡️')

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ['⬅️', '➡️']

            while True:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    break
                else:
                    if str(reaction.emoji) == '➡️':
                        self.current_page += 1
                        if self.current_page >= len(self.help_pages):
                            self.current_page = 0  # Loop back to the first page
                    elif str(reaction.emoji) == '⬅️':
                        self.current_page -= 1
                        if self.current_page < 0:
                            self.current_page = len(self.help_pages) - 1  # Loop to the last page

                    await message.edit(embed=self.help_pages[self.current_page])
                    await message.remove_reaction(reaction, user)

async def setup(bot):
    bot.help_command = None  # Disable default help command
    await bot.add_cog(HelpCommand(bot))
