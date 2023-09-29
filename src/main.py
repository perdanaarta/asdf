import asyncio
import logging
from typing import Optional, List

import discord
from utils.log import logger as log
from discord.ext import commands

class Pinkbot(commands.Bot):
    def __init__(
        self,
        *args,
        command_prefix: str,
        intents: discord.Intents,
        initial_activity: Optional[discord.Activity] = None,
        initial_extensions: List[str],
        testing_guild_id: Optional[int] = None,
        **kwargs
    ) -> None:
        super().__init__(*args, command_prefix=command_prefix, intents=intents, **kwargs)
        self.testing_guild_id = testing_guild_id
        self.initial_extensions = initial_extensions
        self.initial_activity = initial_activity

    async def setup_hook(self) -> None:
        # Load extensions prior to sync to ensure we are syncing interactions defined in those extensions.
        for extension in self.initial_extensions:
            await self.load_extension(f"ext.{extension}")

        # Sync for test guild
        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)

    async def on_ready(self) -> None:
        # Change the initital activity
        if self.initial_activity:
            await self.change_presence(
                activity=self.initial_activity,
                status=discord.Status.online
            )

        # Display info of the bot status
        log.info(f"Connected to Discord (latency: {self.latency*1000:,.0f} ms).")
        log.info(f"{self.user.name} ready.")

async def main():
    exts = ['general']
    async with Pinkbot(
        command_prefix="$",
        intents=discord.Intents.all(),
        initial_extensions=exts,
    ) as bot:
        await bot.start("MTAzMDAzNTYwNzkwMjIzMjY2Nw.GoCTOe.-33F1kVSzqFVweSdk47tL3jlDsiuMx0WaJSZSs")

asyncio.run(main())

