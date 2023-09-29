import discord
from discord.ext.commands import Cog, Bot

class GeneralExtension(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot