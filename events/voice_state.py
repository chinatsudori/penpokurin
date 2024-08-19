import discord
from discord.ext import commands
from helpers.error_handler import send_log_message

class VoiceStateEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.self_video and not before.self_video:
            try:
                await member.move_to(None)  # Disconnect the user from the voice channel

                # Create an embed message
                embed = discord.Embed(
                    title="Disconnected from Voice Channel",
                    description="Webcam usage is not allowed while streaming games.",
                    color=discord.Color.red(),
                )
                embed.set_author(
                    name=self.bot.user.name, icon_url=self.bot.user.avatar.url
                )
                embed.add_field(
                    name="Reason",
                    value="Using webcam while streaming games",
                    inline=False,
                )
                embed.set_footer(text="Please adhere to the server rules.")

                await member.send(embed=embed)
                print(f"Disconnected {member} for using webcam.")

                # Log the disconnect event
                await send_log_message(
                    "Voice Channel Disconnect",
                    f"**Member:** {member}\n**Reason:** Using webcam while streaming games",
                    discord.Color.red(),
                )

            except discord.Forbidden:
                print(f"Insufficient permissions to disconnect {member}.")
            except discord.HTTPException as e:
                print(f"Failed to disconnect {member}: {e}")

async def setup(bot):
    await bot.add_cog(VoiceStateEvents(bot))
