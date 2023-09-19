from .cogs import leetcode
from discord import Intents
from discord.ext import commands
from config import DISCORD_TOKEN
import asyncio


def setup():
    """
    Set up Discord bot with COGs.

    :return: None
    """
    # Set discord intents
    intents = Intents.default()
    intents.message_content = True

    # Initialize bot
    bot = commands.Bot(command_prefix="!", intents=intents)
    asyncio.run(leetcode.setup(bot))

    # Run bot
    bot.run(DISCORD_TOKEN)
