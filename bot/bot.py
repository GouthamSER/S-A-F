from pyrogram import Client, enums, __version__

from . import API_HASH, API_ID, LOGGER, BOT_TOKEN 

from bot.plugins.webcode import bot_run
from os import environ
from aiohttp import web as webserver

PORT_CODE = environ.get("PORT", "8080")

from .user import User

class Bot(Client):
    USER: User = None
    USER_ID: int = None

    def __init__(self):
        super().__init__(
            "bot",
            api_hash=API_HASH,
            api_id=API_ID,
            plugins={
                "root": "bot/plugins"
            },
            workers=200,
            bot_token=BOT_TOKEN,
            sleep_threshold=10
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        
        client = webserver.AppRunner(await bot_run())
        await client.setup()
        bind_address = "0.0.0.0"
        await webserver.TCPSite(client, bind_address,
        PORT_CODE).start()
        
        bot_details = await self.get_me()
        self.set_parse_mode(enums.ParseMode.HTML)
        self.LOGGER(__name__).info(
            f"@{bot_details.username}  started! "
        )
        self.USER, self.USER_ID = await User().start()
        

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. Bye.")
