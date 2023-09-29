from .music import MusicExtension

async def setup(bot):
    await bot.add_cog(MusicExtension(bot))