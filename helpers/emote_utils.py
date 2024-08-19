import re


# Function to extract emote usage
def extract_emote_usage(messages):
    emote_usage = {}
    emote_pattern = re.compile(r"<:\w+:\d+>")

    for message in messages:
        emotes = emote_pattern.findall(message)
        for emote in emotes:
            if emote in emote_usage:
                emote_usage[emote] += 1
            else:
                emote_usage[emote] = 1

    return emote_usage


# Function to fetch chat messages
async def fetch_chat_messages(channels):
    messages = []
    for channel in channels:
        async for message in channel.history(limit=10000):  # Adjust limit as needed
            messages.append(message.content)
    return messages
