from discord.ext import commands
from config import TOKEN, COMMAND_PREFIX, INTENTS
import asyncio
import os
import signal
import sys
from lib.error_handler import setup_logging, log_info, log_error  # Import logging functions

setup_logging()  # Setup logging configuration

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=INTENTS)

async def load_extensions():
    for folder in ["commands", "events", "tasks"]:
        for filename in os.listdir(f"./{folder}"):
            if filename.endswith(".py") and filename != "__init__.py":
                extension = f"{folder}.{filename[:-3]}"
                try:
                    await bot.load_extension(extension)
                    log_info(f"Loaded extension: {extension}")  # Use log_info
                except Exception as e:
                    log_error(f"Failed to load extension {extension}. {e}", exc_info=True)  # Use log_error with traceback

@bot.event
async def on_ready():
    log_info(f"Logged in as {bot.user.name} - {bot.user.id}")  # Use log_info
    log_info("Ready to serve!")  # Use log_info

async def main():
    await load_extensions()
    await bot.start(TOKEN)

def shutdown(signal, loop):
    log_info(f"Received exit signal {signal.name}...")  # Use log_info
    loop.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    if sys.platform != 'win32':
        for s in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown(s, loop)))

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log_info("Bot terminated.")  # Use log_info
    finally:
        for task in asyncio.all_tasks(loop):
            task.cancel()
        loop.close()