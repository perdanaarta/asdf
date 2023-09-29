from .general import GeneralExtension

async def setup(bot):
    await bot.add_cog(GeneralExtension(bot))