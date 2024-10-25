from .currencycon import currencycon


async def setup(bot):
    await bot.add_cog(currencycon(bot)) 