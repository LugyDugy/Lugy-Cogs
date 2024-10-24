from .slashcmds import slashcmds


async def setup(bot):
    await bot.add_cog(slashcmds(bot))