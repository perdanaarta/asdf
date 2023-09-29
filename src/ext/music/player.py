from utils.log import logger as log
from utils.config import Config

import discord
from discord.ext.commands import Bot

import json
import random
import wavelink
import wavelink.ext.spotify as spotify

from .queue import Queue


class Player(wavelink.Player):
    def __init__(self, bot: Bot, channel: discord.VoiceChannel):
        super().__init__(bot, channel)
        self.bot= bot
        self.channel = channel

        self.queue: Queue = Queue()

    async def next(self):
        track = self.queue.next()
        if track is None:
            return
        
        await self.play(track)

    async def previous(self):
        track = self.queue.previous()
        if track is None:
            return
        
        await self.play(track)

class PlayerManager:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.players = {}

        bot.loop.create_task(self.connect_node())

    async def connect_node(self):
        await self.bot.wait_until_ready()

        nodes = json.loads(open(Config.LAVALINK_NODES_JSON).read())
        for node in nodes:
            try:
                await wavelink.NodePool.create_node(
                    bot=self.bot,
                    spotify_client=spotify.SpotifyClient(
                        client_id=Config.SPOTIFY_CLIENT_ID,
                        client_secret=Config.SPOTIFY_CLIENT_SECRET
                    ),
                    **node
                )
            except Exception as e:
                log.error(e)

    async def create_player(self, guild: discord.Guild, channel: discord.VoiceChannel) -> Player:
        if not guild.voice_client:
            player = await channel.connect(cls=Player)
            self.players[guild.id] = player
            return player
        else:
            return self.players[guild.id]

    async def get_player(self, guild: discord.Guild) -> Player | None:
        if not guild.voice_client:
            return None
        else:
            player = self.players[guild.id]
            return player

    async def destroy_player(self, guild: discord.Guild) -> None:
        if not guild.voice_client:
            return

        player = self.players[guild.id]
        del self.players[guild.id]