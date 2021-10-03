import os
import ast
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

if bool(os.environ.get("WEBHOOK", False)):
    from info import Config
else:
    from info import Config

from utils import get_filter_results, get_file_details, is_subscribed, get_poster

from database.filters_mdb import del_all, find_filter

from database.connections_mdb import(
    all_connections,
    active_connection,
    if_active,
    delete_connection,
    make_active,
    make_inactive
)

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
                    [
                        InlineKeyboardButton("⏪BACK", callback_data=f"back_{int(index)+1}_{keyword}"),
                        InlineKeyboardButton(f"ℙ𝔸𝔾𝔼 {int(index)+2}/{data['total']}🔖", callback_data="pages")
                    ]
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
                    [
                        InlineKeyboardButton("⏪", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("⏩", callback_data=f"next_{int(index)+1}_{keyword}"),
                        InlineKeyboardButton(f"ℙ𝔸𝔾𝔼 {int(index)+2}/{data['total']}🔖", callback_data="pages")
                    ]
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
                    [
                        InlineKeyboardButton("NEXT⏩", callback_data=f"next_{int(index)-1}_{keyword}"),
                        InlineKeyboardButton(f"ℙ𝔸𝔾𝔼 {int(index)}/{data['total']}🔖", callback_data="pages")
                    ]
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
                    [
                        InlineKeyboardButton("⏪", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("⏩", callback_data=f"next_{int(index)-1}_{keyword}"),
                        InlineKeyboardButton(f"ℙ𝔸𝔾𝔼 {int(index)}/{data['total']}🔖", callback_data="pages")
                    ]
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
                    InlineKeyboardButton("➕Add me to Group✅", url="https://t.me/PFM_MediaSearchBot?startgroup=true")
                ]
                ]
            await query.message.edit(START_MSG.format(query.from_user.mention), reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "close_data":
            await query.message.delete()

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
                        InlineKeyboardButton('Share', url='https://t.me/share/url?url=%20https://t.me/PrimeFlix_Chats'),
                        InlineKeyboardButton('Channel', url='https://t.me/PrimeFlixMedia_All')
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
                        InlineKeyboardButton('Share', url='https://t.me/share/url?url=%20https://t.me/PrimeFlix_Chats'),
                        InlineKeyboardButton('Channel', url='https://t.me/PrimeFlixMedia_All')
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
            await query.answer("Just a Page. Leave me Alone❗.",show_alert=True)

        elif query.data == "admn_list":
            await query.answer("Tag any one of these ADMINS:\n\n@CLaY995\n@nakul006\n@N_i_8_m_a_r_e\n@RFt_CyberPro", show_alert=True)

        elif query.data == "delallconfirm":
            userid = query.from_user.id
            chat_type = query.message.chat.type

            if chat_type == "private":
                grpid  = await active_connection(str(userid))
                if grpid is not None:
                    grp_id = grpid
                    try:
                        chat = await client.get_chat(grpid)
                        title = chat.title
                    except:
                        await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
                        return
                else:
                    await query.message.edit_text(
                        "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                        quote=True
                    )
                    return

