import discord
from discord.ext import commands
from helpers.error_handler import send_log_message

class ServerLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await send_log_message(
            "Message Deleted",
            f"**Author:** {message.author}\n**Channel:** {message.channel}\n**Content:** {message.content}",
            discord.Color.red(),
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await send_log_message(
            "Message Edited",
            f"**Author:** {before.author}\n**Channel:** {before.channel}\n**Before:** {before.content}\n**After:** {after.content}",
            discord.Color.orange(),
        )

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        changes = []
        if before.roles != after.roles:
            changes.append("Roles")
        if before.nick != after.nick:  # Check if the nickname has changed
            changes.append("Nickname")
        if before.avatar != after.avatar:
            changes.append("Avatar")
        if changes:
            await send_log_message(
                "Member Updated",
                f"**Member:** {after}\n**Changes:** {', '.join(changes)}",
                discord.Color.gold(),
            )

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        await send_log_message(
            "Member Banned",
            f"**User:** {user.name}",
            discord.Color.red(),
        )

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        await send_log_message(
            "Member Unbanned",
            f"**User:** {user.name}",
            discord.Color.green(),
        )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await send_log_message(
            "Member Joined",
            f"**Member:** {member.name}",
            discord.Color.green(),
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await send_log_message(
            "Member Left",
            f"**Member:** {member.name}",
            discord.Color.red(),
        )

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        await send_log_message(
            "Channel Created",
            f"**Channel:** {channel.name}",
            discord.Color.green(),
        )

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        await send_log_message(
            "Channel Deleted",
            f"**Channel:** {channel.name}",
            discord.Color.red(),
        )

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        await send_log_message(
            "Channel Updated",
            f"**Before:** {before.name}\n**After:** {after.name}",
            discord.Color.orange(),
        )

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        await send_log_message(
            "Role Created",
            f"**Role:** {role.name}",
            discord.Color.green(),
        )

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        await send_log_message(
            "Role Deleted",
            f"**Role:** {role.name}",
            discord.Color.red(),
        )

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        await send_log_message(
            "Role Updated",
            f"**Before:** {before.name}\n**After:** {after.name}",
            discord.Color.orange(),
        )

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        await send_log_message(
            "Server Updated",
            "The server's settings have been updated.",
            discord.Color.blue(),
        )

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        await send_log_message(
            "Invite Created",
            f"**Invite:** {invite.url}",
            discord.Color.green(),
        )

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        await send_log_message(
            "Invite Deleted",
            f"**Invite:** {invite.url}",
            discord.Color.red(),
        )

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        await send_log_message(
            "Emojis Updated",
            "The server's emojis have been updated.",
            discord.Color.blue(),
        )

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel != after.channel:
            await send_log_message(
                "Voice Channel Switched",
                f"**Member:** {member.name}\n**From:** {before.channel}\n**To:** {after.channel}",
                discord.Color.purple(),
            )

async def setup(bot):
    await bot.add_cog(ServerLogger(bot))
