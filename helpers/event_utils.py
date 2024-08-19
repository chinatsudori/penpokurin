import json
import re
import discord
import io
from PIL import Image
from helpers.time_utils import (
    parse_date_str,
    utc_from_timestamp,
    iso_format,
    dt,
    add_hours_to_time,
)
from config import LOG_CHANNEL_ID

async def send_log_message(self, message):
    log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(message)
    else:
        print(f"Log channel {LOG_CHANNEL_ID} not found.")


def generate_placeholder_image():
    """Generate a placeholder image."""
    width, height = 100, 100
    color = (255, 0, 0)  # Red color
    image = Image.new("RGB", (width, height), color)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()



async def create_or_update_discord_event(bot, guild_id, event_data):
    """Create or update a Discord event."""
    print("Creating/updating event with data:", event_data)  # Debugging
    try:
        guild = bot.get_guild(guild_id)
        if not guild:
            raise ValueError("Guild not found")

        if "2x" in event_data.get("description", ""):
            print("Skipping event with '2x' in the description")
            return None

        start_time = event_data.get("start_time")
        end_time = event_data.get("end_time")
        if isinstance(start_time, str):
            start_time = parse_date_str(start_time)
        if isinstance(end_time, str):
            end_time = parse_date_str(end_time)

        if not isinstance(start_time, dt) or (end_time and not isinstance(end_time, dt)):
            raise ValueError(
                "start_time and end_time must be timezone-aware datetime objects"
            )

        location = event_data.get("location") or ""
        image = event_data.get("image")
        reason = event_data.get("reason") or ""

        if isinstance(image, str):
            image = image.encode()

        existing_events = await guild.fetch_scheduled_events()
        for existing_event in existing_events:
            if (
                existing_event.name == event_data["description"]
                and existing_event.start_time == start_time
            ):
                await existing_event.edit(
                    name=event_data["description"],
                    description=event_data["name"],
                    start_time=start_time,
                    end_time=end_time,
                    location=location,
                    image=image,
                    reason=reason,
                )
                return existing_event

        event = await guild.create_scheduled_event(
            name=event_data["description"],
            description=event_data["name"],
            start_time=start_time,
            end_time=end_time,
            privacy_level=discord.PrivacyLevel.guild_only,
            entity_type=discord.EntityType.external,
            location=location,
            image=image,
            reason=reason,
        )
        return event
    except Exception as e:
        print(f"An error occurred while creating/updating the event: {e}")
        await send_log_message(
            bot,
            "Event Creation/Update Error",
            f"**Error:** {e}\n**Event Data:** {json.dumps(event_data)}",
            discord.Color.red()
        )
        raise


async def delete_events_not_in_json(bot, guild_id, events_data):
    """Delete events that are not in the provided JSON."""
    print("Deleting events not in JSON")  # Debugging
    try:
        guild = bot.get_guild(guild_id)
        if not guild:
            raise ValueError("Guild not found")

        existing_events = await guild.fetch_scheduled_events()
        event_names = {event["description"] for event in events_data}

        for existing_event in existing_events:
            if existing_event.name not in event_names:
                await existing_event.delete()
                print(f"Deleted event: {existing_event.name}")

    except Exception as e:
        print(f"An error occurred while deleting events: {e}")
        await send_log_message(
            bot,
            "Event Deletion Error",
            f"**Error:** {e}",
            discord.Color.red()
        )
        raise


def parse_json_to_events(json_data):
    """Parse JSON dictionary to extract events."""
    if not isinstance(json_data, dict):
        raise ValueError(f"Expected a dictionary, got {type(json_data).__name__}.")

    print("Parsing JSON data:", json_data)  # Debugging

    description = json_data.get("description", "")
    if description is None:
        raise ValueError("Description is None")

    lines = description.split("\n")
    events = []
    is_upcoming_events = False

    timestamp_pattern = r"<t:\d+:[RF]>"  # Regex pattern to match timestamps

    for line in lines:
        if line.startswith("**Upcoming Events**"):
            is_upcoming_events = True
            continue
        elif line.startswith("**Ending Soon [Currently Ongoing]**"):
            is_upcoming_events = False
            continue

        if is_upcoming_events:
            line_no_timestamp = re.sub(timestamp_pattern, "", line).strip()
            if line_no_timestamp:
                print("Processing line:", line_no_timestamp)

                timestamp_pattern = r"<t:(\d+):[RF]>"
                matches = re.findall(timestamp_pattern, line)

                for match in matches:
                    timestamp = int(match)
                    timestamp_dt = utc_from_timestamp(timestamp)

                    end_time = add_hours_to_time(timestamp_dt, 1)

                    events.append(
                        {
                            "name": "Upcoming Event",
                            "description": line_no_timestamp,
                            "start_time": iso_format(timestamp_dt),
                            "end_time": iso_format(end_time),
                            "entity_type": 3,  # Example entity type (3 for external)
                            "privacy_level": 2,  # Example privacy level (2 for guild_only)
                            "channel_id": 710175169003520060,  # Specify channel_id if necessary
                            "entity_metadata": create_entity_metadata(3, "Location"),
                            "location": "Location",
                            "image": generate_placeholder_image(),
                            "reason": "Carl Import",
                        }
                    )

    if not events:
        print("No events found in the provided JSON.")
    return events


async def send_scheduled_event_embed(ctx, json_data):
    """Convert JSON data into a rich embed and send it."""
    embed = discord.Embed(
        title=json_data.get("title", "No Title"),
        description=json_data.get("description", ""),
        color=json_data.get("color", 3447003),
    )

    footer = json_data.get("footer", {})
    if "text" in footer:
        embed.set_footer(text=footer["text"])

    fields = json_data.get("fields", [])
    for field in fields:
        name = field.get("name", "No Name")
        value = field.get("value", "No Value")
        inline = field.get("inline", False)
        embed.add_field(name=name, value=value, inline=inline)

    await ctx.send(embed=embed)



async def parse_json_string(json_str):
    """Parse a JSON string to a dictionary."""
    try:
        json_data = json.loads(json_str)
        print("Parsed JSON data:", json_data)  # Debugging
        return json_data
    except json.JSONDecodeError as e:
        await send_log_message(
            bot,
            "JSON Parsing Error",
            f"**Error:** Invalid JSON\n**Details:** {e}",
            discord.Color.red()
        )
        raise ValueError(f"Invalid JSON: {e}")


def create_entity_metadata(entity_type, location=""):
    """Create metadata for the event based on entity type."""
    if entity_type == 3:  # External event type
        return {"location": location}
    return {}
