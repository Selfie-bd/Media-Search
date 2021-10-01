import re
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, START_MSG, ADMINS

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from info import AUTH_GROUPS
from pyrogram import Client, filters
from utils import get_filter_results, get_file_details, is_subscribed, get_poster


BUTTONS = {}
BOT = {}


@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        up_search = search.upper()
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            btn.append(
                   [
                       InlineKeyboardButton("🎥:MOVIES✅", url="https://t.me/joinchat/dZmnXiQ5a2ViMWZl"),
                       InlineKeyboardButton("📽:SERIES✅", url="https://t.me/joinchat/vz04fx0LgSI5MzZl")
                   ]
               )
            for file in files:
                file_id = file.file_id
                filename = f"📀:[{get_size(file.file_size)}]📂{file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=subinps_-_-_-_{file_id}")]
                )
        else:
            return
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="🔖 ℙ𝔸𝔾𝔼 1/1🔖",callback_data="pages")]
            )
            buttons.append(
                [InlineKeyboardButton(text="🇸‌🇭‌🇦‌🇷‌🇪‌-🇱‌🇮‌🇳‌🇰‌", url="https://t.me/share/url?url=%20https://t.me/PrimeFlix_Chats")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"🇵‌🇫‌🇲 ᶜʰᵃᵗˢ \n\n𝐅𝐨𝐫: <b>{message.from_user.mention}</b>\n\n🎬 𝐌𝐨𝐯𝐢𝐞/𝐒𝐞𝐫𝐢𝐞𝐬: {up_search}\n🌩️ 𝐓𝐨𝐭𝐚𝐥 𝐑𝐞𝐬𝐮𝐥𝐭𝐬: {len(btn)}\n\n© @PrimeFlixMedia_All­  ­  ­  ­  ­  ", reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_text(f"🇵‌🇫‌🇲 ᶜʰᵃᵗˢ \n‌\n𝐅𝐨𝐫: <b>{message.from_user.mention}</b>\n\n🎬 𝐌𝐨𝐯𝐢𝐞/𝐒𝐞𝐫𝐢𝐞𝐬: {up_search}\n🌩️ 𝐓𝐨𝐭𝐚𝐥 𝐑𝐞𝐬𝐮𝐥𝐭𝐬: {len(btn)}\n\n© @PrimeFlixMedia_All ­  ­  ­  ­  ­  ", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"🔖 ℙ𝔸𝔾𝔼 1/{data['total']}🔖",callback_data="pages")]
        )
        buttons.append(
            [InlineKeyboardButton(text="🇸‌🇭‌🇦‌🇷‌🇪‌-🇱‌🇮‌🇳‌🇰‌", url="https://t.me/share/url?url=%20https://t.me/PrimeFlix_Chats")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"🇵‌🇫‌🇲 ᶜʰᵃᵗˢ \n\n𝐅𝐨𝐫: <b>{message.from_user.mention}</b>\n\n🎬 𝐌𝐨𝐯𝐢𝐞/𝐒𝐞𝐫𝐢𝐞𝐬: {up_search}\n🌩️ 𝐓𝐨𝐭𝐚𝐥 𝐑𝐞𝐬𝐮𝐥𝐭𝐬: {len(btn)}\n\n© @PrimeFlixMedia_All   ­  ­  ­  ­  ", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"🇵‌🇫‌🇲 ᶜʰᵃᵗˢ \n\n𝐅𝐨𝐫: <b>{message.from_user.mention}</b>\n\n🎬 𝐌𝐨𝐯𝐢𝐞/𝐒𝐞𝐫𝐢𝐞𝐬: {up_search}\n🌩 𝐓𝐨𝐭𝐚𝐥 𝐑𝐞𝐬𝐮𝐥𝐭𝐬: {len(btn)}\n\n© @PrimeFlixMedia_All ‌‎ ­  ­  ­  ­  ­  ", reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          
