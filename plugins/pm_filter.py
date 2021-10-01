#Edited by @CLaY995
import os
import ast
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, START_MSG, ADMINS
from sample_info import HELP_TEXT, MAL_HELP_TXT, HELP_MSG
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
from pyrogram.errors import UserNotParticipant
from utils import get_filter_results, get_file_details, is_subscribed, get_poster


BUTTONS = {}
BOT = {}
@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**⚠️Join My Channel to use this Bot!⚠️**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("♻️Join our Channel♻️", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        up_search = search.upper()
        files = await get_filter_results(query=search)
        if files:
            btn.append(
                   [
                       InlineKeyboardButton("🎥:мσνιєѕ⭕", url="https://t.me/joinchat/dZmnXiQ5a2ViMWZl"),
                       InlineKeyboardButton("📽:ѕєяιєѕ⭕", url="https://t.me/joinchat/vz04fx0LgSI5MzZl")
                   ]
               )
            for file in files:
                file_id = file.file_id
                filename = f"💽:[{get_size(file.file_size)}]📂{file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"subinps#{file_id}")]
                    )
        else:
            await message.reply_text(
                text="▫️ <b>Oops❗ the Movie that you Requested for is not in my Database 🌩️.</b>\n\n📍 <b>Ask the Admins to Upload the Files to my DB 🗃️.</b>",
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup(
                     [
                         [
                             InlineKeyboardButton("Request Here ♻️", url="https://t.me/PrimeFlix_Chats")
                         ]
                     ]
                ),
                reply_to_message_id=message.message_id
            )
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
                await message.reply_photo(photo=poster, caption=f"🇵‌🇫‌🇲 ᶜʰᵃᵗˢ \n\n𝐅𝐨𝐫: <b>{message.from_user.mention}</b>\n\n🎬 𝐌𝐨𝐯𝐢𝐞/𝐒𝐞𝐫𝐢𝐞𝐬: {up_search}\n🌩️ 𝐓𝐨𝐭𝐚𝐥 𝐑𝐞𝐬𝐮𝐥𝐭𝐬: {len(btn)}\n\n© @PrimeFlixMedia_All ‌‌‌‌‎ ­  ­ ", reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_text(f"🇵‌🇫‌🇲 ᶜʰᵃᵗˢ \n\n𝐅𝐨𝐫: <b>{message.from_user.mention}</b>\n\n🎬 𝐌𝐨𝐯𝐢𝐞/𝐒𝐞𝐫𝐢𝐞𝐬: {up_search}‌‎\n🌩️ 𝐓𝐨𝐭𝐚𝐥 𝐑𝐞𝐬𝐮𝐥𝐭𝐬: {len(btn)}\n\n© @PrimeFlixMedia_All ‌‌‌‌‎ ­  ­  ­  ­  ­", reply_markup=InlineKeyboardMarkup(buttons))
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
            await message.reply_photo(photo=poster, caption=f"🇵‌🇫‌🇲 ᶜʰᵃᵗˢ \n\n𝐅𝐨𝐫: <b>{message.from_user.mention}</b>\n\n🎬 𝐌𝐨𝐯𝐢𝐞/𝐒𝐞𝐫𝐢𝐞𝐬: {up_search}\n🌩️ 𝐓𝐨𝐭𝐚𝐥 𝐑𝐞𝐬𝐮𝐥𝐭𝐬: {len(btn)}\n\n© @PrimeFlixMedia_All ‌‌‌‌‎ ­  ­  ­  ­  ­  ", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"🇵‌🇫‌🇲 ᶜʰᵃᵗˢ \n\n𝐅𝐨𝐫: <b>{message.from_user.mention}</b>\n\n🎬 𝐌𝐨𝐯𝐢𝐞/𝐒𝐞𝐫𝐢𝐞𝐬: {up_search}\n🌩️ 𝐓𝐨𝐭𝐚𝐥 𝐑𝐞𝐬𝐮𝐥𝐭𝐬: {len(btn)}\n\n© @PrimeFlixMedia_All ‌‌‌‌‎ ­  ­  ­  ­  ­  ", reply_markup=InlineKeyboardMarkup(buttons))


