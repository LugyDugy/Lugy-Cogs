import discord
import aiohttp

from redbot.core import commands, app_commands
from redbot.core.bot import Red

class currencycon(commands.Cog):
    """
    currency converter inspired by TrustyJAID's 
    conversions cog, tweaked to work with
    slash commands
    """

    __author__ = ["Lugy"]
    __version__ = "0.3"

    def __init__(self, bot: Red):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @app_commands.command()
    async def currency_convert(
        self,
        ctx: commands.Context,
        money1: str,
        money2: str,
        total: float = 1.0,
    ):
        money1 = money1.upper()
        money2 = money2.upper()

        if len(money1) != 3:
            await ctx.maybe_send_embed(
                (
                    f"{money1} is formatted incorrectly"
                )
            )
            return
        convert = await self.conversion(money1, money2)
        if convert == None:
             await ctx.maybe_send_embed(
                  f"Invalid request, killing self"
             )
             return
        verted = convert * total
        await ctx.response.send_message(f"{total} {money1} == {verted:,.2f} {money2}")

    async def conversion(
              self,
              money1: str,
              money2: str,
    ):
         convert = None
         url = f"https://query1.finance.yahoo.com/v8/finance/chart/{money1}{money2}=x"
         async with self.session.get(url) as query:
            queryinfo = await query.json()
         data = queryinfo.get("chart", {}).get("result", [])
         convert = data[0].get("meta", {}).get("regularMarketPrice")
         return convert