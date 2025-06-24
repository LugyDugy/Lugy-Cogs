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
    __version__ = "1.1.2"

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
            await ctx.response.send_message(
                (
                    f"{money1} is formatted incorrectly"
                )
            )
            return
        convert = await self.conversion(money1, money2)
        if convert == None:
             await ctx.response.send_message(
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
        try:
            log = None
            convert = None
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", 
                       "Accept": "application/json" 
                      }
            url = f"https://open.er-api.com/v6/latest/{money1}"
            async with self.session.get(url, headers=headers) as query:
                queryinfo = await query.json()
            convert = queryinfo.get("{money2}")
        except Exception:
            log.exception(f"Could not complete request")
        return convert