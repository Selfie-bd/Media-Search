#Edited by @CLaY995
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, START_MSG
from sample_info import HELP_TEXT, MAL_HELP_TXT
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
            await client.send_message(
                chat_id=message.from_user.id, 
                text="<b>📍 #UserNotice:</b>\n\n▫️ <b>Request for Movies in the Group Link given below.</b>\n\n▫️ <b>The PM Request Function is Taken down. Sorry for the inconvenience 🙂</b>", 
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup(
                     [
                         [
                             InlineKeyboardButton("Request Group ♻️", url="https://t.me/PrimeFlix_Chats")
                         ]
                     ]
                )
            )
        else:
            await client.reply_text(
                chat_id=message.from_user.id,
                text="▫️ <b>Oops❗ the Movie that you Requested for is not in my Database 🌩️.</b>\n\n📍 <b>Ask the Admins to Upload the Files to my DB 🗃️.</b>",
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup(
                     [
                         [
                             InlineKeyboardButton("Request Here ♻️", url="https://t.me/PrimeFlix_Chats")
                         ]
                     ]
                )
            )
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
            await client.reply_text(
                chat_id=message.from_user.id,
                text="▫️ <b>Oops❗ the Movie that you Requested for is not in my Database 🌩️.</b>\n\n📍 <b>Ask the Admins to Upload the Files to my DB 🗃️.</b>",
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup(
                     [
                          [
                               InlineKeyboardButton("Admin List 💫", callback_data="admn_list")
                          ]
                     ]
                )
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
            await message.reply_text(f"🇵‌🇫‌🇲 ᶜʰᵃᵗˢ \n\n𝐅𝐨𝐫: <b>{message.from_user.mention}</b>\n\n🎬 𝐌𝐨𝐯𝐢𝐞/𝐒𝐞𝐫𝐢𝐞𝐬: {up_search}\n🌩 𝐓𝐨𝐭𝐚𝐥 𝐑𝐞𝐬𝐮𝐥𝐭𝐬: {len(btn)}\n\n© @PrimeFlixMedia_All ‌‌‌‌‎ ­  ­  ­  ­  ­  ", reply_markup=InlineKeyboardMarkup(buttons))

    
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



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪BACK", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🔖 ℙ𝔸𝔾𝔼 {int(index)+2}/{data['total']}🔖", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton(text="🇸‌🇭‌🇦‌🇷‌🇪‌-🇱‌🇮‌🇳‌🇰‌", url="https://t.me/share/url?url=%20https://t.me/PrimeFlix_Chats")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪BACK", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🔖 ℙ𝔸𝔾𝔼 {int(index)+2}/{data['total']}🔖", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton(text="🇸‌🇭‌🇦‌🇷‌🇪‌-🇱‌🇮‌🇳‌🇰‌", url="https://t.me/share/url?url=%20https://t.me/PrimeFlix_Chats")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("NEXT⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🔖 ℙ𝔸𝔾𝔼 {int(index)}/{data['total']}🔖", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton(text="🇸‌🇭‌🇦‌🇷‌🇪‌-🇱‌🇮‌🇳‌🇰‌", url="https://t.me/share/url?url=%20https://t.me/PrimeFlix_Chats")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪BACK", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🔖 ℙ𝔸𝔾𝔼 {int(index)}/{data['total']}🔖", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton(text="🇸‌🇭‌🇦‌🇷‌🇪‌-🇱‌🇮‌🇳‌🇰‌", url="https://t.me/share/url?url=%20https://t.me/PrimeFlix_Chats")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "start":
            buttons = [
                [
                    InlineKeyboardButton("My-CreatoR🧑‍💻", url="https://t.me/CLaY995")
                ],
                [
                    InlineKeyboardButton("🔎 Search Here", switch_inline_query_current_chat=''),
                    InlineKeyboardButton("🔗 Our-LinkZ", url="https://t.me/PrimeFlixMedia_All")
                ],
                [
                    InlineKeyboardButton("About", callback_data="about"),
                    InlineKeyboardButton("Help", callback_data="help")
                ],
                [
                    InlineKeyboardButton("➕Add me to Group✅", url="https://t.me/PFM_MediaSearchBot?startgroup=true")
                ]
                ]
            await query.message.edit(START_MSG.format(query.from_user.mention), reply_markup=InlineKeyboardMarkup(buttons), parse_mode="html", disable_web_page_preview=True)

        elif query.data == "about":
            buttons = [
                [
                    InlineKeyboardButton('My LinkZ', url='https://t.me/PrimeFlixMedia_All'),
                    InlineKeyboardButton('Source-Code', url='https://t.me/Oomban_ULLATH')
                ],
                [
                    InlineKeyboardButton('Back', callback_data='start')
                ]
                ]
            await query.message.edit(text="<b>🧑‍💻Creator : <a href='https://t.me/ClaeyZ_UBot'>CLÆ͜͡Ｙ</a>\n🤩Available to EVERYONE\n🌏Language : <code>Python3</code>\n📚Library : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio</a>\n📋Source-Code : <a href='https://t.me/Oomban_ULLATH'>🔘Click here</a>\n📡Ma-Channel : <a href='https://t.me/PrimeFlixMedia_All'>PFM Links</a> </b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=False)

        elif query.data == "help":
            buttons = [
                [
                    InlineKeyboardButton('Malayalam Translation 🌐', callback_data='mal_help')
                ],
                [
                    InlineKeyboardButton('🏡 Home', callback_data='start'),
                    InlineKeyboardButton('👤 About', callback_data='about')
                ]
                ]
            await query.message.edit(HELP_TEXT, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
            
        elif query.data == "mal_help":
            buttons = [
                [
                    InlineKeyboardButton('🏡 Home', callback_data='start'),
                    InlineKeyboardButton('👤 About', callback_data='about')
                ]
                ]
            await query.message.edit(MAL_HELP_TXT, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data.startswith("subinps"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('📡sʜᴀʀᴇ📡', url='https://t.me/share/url?url=%20https://t.me/PrimeFlix_Chats'),
                        InlineKeyboardButton('Our-LinkZ', url='https://t.me/PrimeFlixMedia_All')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒. Subscribe the CHANNEL😑",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton(' 📡sʜᴀʀᴇ📡', url='https://t.me/share/url?url=%20https://t.me/PrimeFlix_Chats'),
                        InlineKeyboardButton('Our-LinkZ', url='https://t.me/PrimeFlixMedia_All')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )


        elif query.data == "pages":
            await query.answer()
    else:
        await query.answer("😑This is NOT for YoU❗, Search Up on ur Own",show_alert=True)

    elif query.data == "admn_list":
          await query.answer()
    else:
        await query.answer("Tag any one of these ADMINS:\n\n@CLaY995\n@nakul006\n@N_i_8_m_a_r_e\n@RFt_CyberPro", show_alert=True)
  
