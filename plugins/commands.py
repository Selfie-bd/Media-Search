# Code Edited by @CLaY995
import os
import math
import json
import time
import shutil
import heroku3
import requests

if bool(os.environ.get("WEBHOOK", False)):
    from info import SAVE_USER, HEROKU_API_KEY, BOT_START_TIME, AUTH_USERS_2
else:
    from info import SAVE_USER, HEROKU_API_KEY, BOT_START_TIME, AUTH_USERS_2


import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import START_MSG, CHANNELS, ADMINS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION
from sample_info import HELP_TEXT, MAL_HELP_TXT
from utils import Media, get_file_details
from pyrogram.errors import UserNotParticipant
from database.users_mdb import add_user, find_user, all_users
from database.filters_mdb import filter_stats
from plugins.helpers import humanbytes
logger = logging.getLogger(__name__)
bot_logo = "https://telegra.ph/file/a78259e021cf8dba5335d.jpg"

@Client.on_message(filters.command("start"))
async def start(bot, cmd):
    usr_cmdall1 = cmd.text
    if usr_cmdall1.startswith("/start subinps"):
        if AUTH_CHANNEL:
            invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
            try:
                user = await bot.get_chat_member(int(AUTH_CHANNEL), cmd.from_user.id)
                if user.status == "kicked":
                    await bot.send_message(
                        chat_id=cmd.from_user.id,
                        text="Sorry Sir, You are Banned to use me.",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                ident, file_id = cmd.text.split("_-_-_-_")
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text='**1️⃣: Join the CHANNEL & Click "Try Again".**',
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("♻️Join the CHANNEL♻️", url=invite_link.invite_link)
                            ],
                            [
                                InlineKeyboardButton(" 🔄 Try Again", callback_data=f"checksub#{file_id}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text="Something went Wrong.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        try:
            ident, file_id = cmd.text.split("_-_-_-_")
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
                        InlineKeyboardButton('📡sʜᴀʀᴇ & sᴜᴘᴘᴏʀᴛ📡', url='https://t.me/share/url?url=%20https://t.me/PrimeFlix_Chats')
                    ],
                    [
                        InlineKeyboardButton('📼 Channel Links 📼', url='https://t.me/PrimeFlixMedia_All')
                    ]
                    ]
                await bot.send_cached_media(
                    chat_id=cmd.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        except Exception as err:
            await cmd.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")
    elif len(cmd.command) > 1 and cmd.command[1] == 'subscribe':
        invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="**Join My Channel to use this Bot!**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("♻️Join our CHANNEL♻️", url=invite_link.invite_link)
                    ]
                ]
            )
        )
    else:
        await cmd.reply_photo(
            photo=bot_logo,
            caption=START_MSG.format(cmd.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("➕Add me to Group✅", url="https://t.me/PFM_MediaSearchBot?startgroup=true")
                    ]
                ]
            )
        )
        if SAVE_USER == "yes":
            try:
                await add_user(
                    str(message.from_user.id),
                    str(message.from_user.username),
                    str(message.from_user.first_name + " " + (message.from_user.last_name or "")),
                    str(message.from_user.dc_id)
                )
            except:
                pass

@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**🇹‌🇴‌🇹‌🇦‌🇱:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)


@Client.on_message(filters.command('total') & filters.user(ADMINS))
async def total(bot, message):
    """Show total files in database"""
    msg = await message.reply("Processing...⏳", quote=True)
    try:
        total = await Media.count_documents()
        await msg.edit(f'🇹‌🇴‌🇹‌🇦‌🇱‌ 🇫‌🇮‌🇱‌🇪‌🇸‌🗃️: {total}')
    except Exception as e:
        logger.exception('Failed to check total files')
        await msg.edit(f'Error: {e}')


@Client.on_message(filters.command('logger') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))


@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not supported file format')
        return

    result = await Media.collection.delete_one({
        'file_name': media.file_name,
        'file_size': media.file_size,
        'mime_type': media.mime_type
    })
    if result.deleted_count:
        await msg.edit('File is successfully deleted from database')
    else:
        await msg.edit('File not found in database')
@Client.on_message(filters.command('about'))
async def bot_info(bot, message):
    buttons = [
        [
            InlineKeyboardButton('❌ Close', callback_data='close_data'),
            InlineKeyboardButton('📋 Source', url='https://t.me/Oomban_ULLATH')
        ],
        [
            InlineKeyboardButton('♻️ Channel ♻️', url='https://t.me/PrimeFlixMedia_All')
        ]
        ]
    await message.reply(text="<b>🧑‍🔬 Created By: <a href='https://t.me/CLaY995'>CLAEY</a>\n\n🌏 Language: <code>Python3</code>\n⛓️ Server: Heroku\n🌩️ Database: MongoDB\n\n📚 Library: <a href='https://docs.pyrogram.org/'>Pyrogram asyncio</a>\n📋 Source Code: <a href='https://t.me/Oomban_ULLATH'>Click here</a>\n♻️ Channel: <a href='https://t.me/PrimeFlixMedia_All'>👉😁😁👈</a>\n⚙️ **Edited V of Media-Search-Bot** </b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

@Client.on_message(filters.command('help'))
async def help(bot, message):
    buttons = [
        [
            InlineKeyboardButton('❌ Close', callback_data='close_data'),
            InlineKeyboardButton('📋 Source', url='https://t.me/Oomban_ULLATH')
        ],
        [
            InlineKeyboardButton('♻️ Channel ♻️', url='https://t.me/PrimeFlixMedia_All')
        ]
        ]
    await message.reply(HELP_TEXT, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

@Client.on_message(filters.command(["me"]))
async def mera_links(bot, message):
    buttons = [
        [
            InlineKeyboardButton('Movies 🎞️:', callback_data='ignore'),
            InlineKeyboardButton('🔘 Click Here', url='https://t.me/joinchat/dZmnXiQ5a2ViMWZl')
        ],
        [
            InlineKeyboardButton('Series 🎬:', callback_data='ignore'),
            InlineKeyboardButton('🔘 Click Here', url='https://t.me/joinchat/vz04fx0LgSI5MzZl')
        ],
        [
            InlineKeyboardButton('🔗 Other Links 🔗', url='https://t.me/PrimeFlixMedia_All')
        ],
        [
            InlineKeyboardButton('🇸‌🇭‌🇦‌🇷‌🇪‌', url='https://t.me/share/url?url=%20https://t.me/PrimeFlix_Chats')
        ]
        ]
    await message.reply_text(text='**PFM Links..👇✨. Join & Support ✨**', reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True, reply_to_message_id=message.from_user.id)

@Client.on_message(filters.command(["reqformat"]))
async def reqformat(bot, message):
    req_txt = """
▫️𝐌𝐨𝐯𝐢𝐞𝐬/𝐒𝐞𝐫𝐢𝐞𝐬 𝐫𝐞𝐪𝐮𝐞𝐬𝐭 𝐟𝐨𝐫𝐦𝐚𝐭:

▪️**𝙼𝚘𝚟𝚒𝚎 𝙽𝚊𝚖𝚎 + 𝚈𝚎𝚊𝚛**

▪️#𝐄𝐱𝐚𝐦𝐩𝐥𝐞: Avatar 2009, Inception 2010..

▫️𝐖𝐡𝐢𝐥𝐞 𝐑𝐞𝐪𝐮𝐞𝐬𝐭𝐢𝐧𝐠 𝐚𝐥𝐰𝐚𝐲𝐬 𝐫𝐞𝐦𝐞𝐦𝐛𝐞𝐫 𝐭𝐨 𝐬𝐞𝐧𝐝 𝐭𝐡𝐞 𝐜𝐨𝐫𝐫𝐞𝐜𝐭 𝐌𝐨𝐯𝐢𝐞/𝐒𝐞𝐫𝐢𝐞𝐬 𝐍𝐚𝐦𝐞.
▫️#ᴛɪᴘ: 𝐂𝐨𝐩𝐲-𝐏𝐚𝐬𝐭𝐞 𝐭𝐡𝐞 𝐌𝐨𝐯𝐢𝐞 𝐍𝐚𝐦𝐞 𝐟𝐫𝐨𝐦 𝐆𝐨𝐨𝐠𝐥𝐞.
"""
    buttons = [
        [
            InlineKeyboardButton('🇸‌🇭‌🇦‌🇷‌🇪‌', url='https://t.me/share/url?url=%20https://t.me/PrimeFlix_Chats')
        ]
        ]
    await message.reply_text(text=req_txt, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True, reply_to_message_id=message.from_user.id)

@Client.on_message(filters.command('info') & (filters.private | filters.group))
async def showinfo(client, message):
    try:
        cmd, id = message.text.split(" ", 1)
    except:
        id = False
        pass

    if id:
        if (len(id) == 10 or len(id) == 9):
            try:
                checkid = int(id)
            except:
                await message.reply_text("__Enter a valid USER ID__", quote=True, parse_mode="md")
                return
        else:
            await message.reply_text("__Enter a valid USER ID__", quote=True, parse_mode="md")
            return           

        if SAVE_USER == "yes":
            name, username, dcid = await find_user(str(id))
        else:
            try:
                user = await client.get_users(int(id))
                name = str(user.first_name + (user.last_name or ""))
                username = user.username
                dcid = user.dc_id
            except:
                name = False
                pass

        if not name:
            await message.reply_text("__USER Details not found!!__", quote=True, parse_mode="md")
            return
    else:
        if message.reply_to_message:
            name = str(message.reply_to_message.from_user.first_name\
                    + (message.reply_to_message.from_user.last_name or ""))
            id = message.reply_to_message.from_user.id
            username = message.reply_to_message.from_user.username
            dcid = message.reply_to_message.from_user.dc_id
        else:
            name = str(message.from_user.first_name\
                    + (message.from_user.last_name or ""))
            id = message.from_user.id
            username = message.from_user.username
            dcid = message.from_user.dc_id
    
    if not str(username) == "None":
        user_name = f"@{username}"
    else:
        user_name = "none"

    await message.reply_text(
        f"<b>Name</b> : {name}\n\n"
        f"<b>User ID</b> : <code>{id}</code>\n\n"
        f"<b>Username</b> : {user_name}\n\n"
        f"<b>Permanant USER link</b> : <a href='tg://user?id={id}'>Click here!</a>\n\n"
        f"<b>DC ID</b> : {dcid}\n\n",
        quote=True,
        parse_mode="html"
    )

@Client.on_message((filters.private | filters.group) & filters.command('status'))
async def bot_status(client,message):
    if str(message.from_user.id) not in AUTH_USERS_2:
        await message.reply("You are not an Auth User.", quote=True)
        return

    chats, filters = await filter_stats()

    if SAVE_USER == "yes":
        users = await all_users()
        userstats = f"😁 {users} 𝐮𝐬𝐞𝐫𝐬 𝐡𝐚𝐯𝐞 𝐬𝐭𝐚𝐫𝐭𝐞𝐝 𝐌𝐞!\n"
    else:
        userstats = ""

    if HEROKU_API_KEY:
        try:
            server = heroku3.from_key(HEROKU_API_KEY)

            user_agent = (
                'Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/80.0.3987.149 Mobile Safari/537.36'
            )
            accountid = server.account().id
            headers = {
            'User-Agent': user_agent,
            'Authorization': f'Bearer {HEROKU_API_KEY}',
            'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
            }

            path = "/accounts/" + accountid + "/actions/get-quota"

            request = requests.get("https://api.heroku.com" + path, headers=headers)

            if request.status_code == 200:
                result = request.json()

                total_quota = result['account_quota']
                quota_used = result['quota_used']

                quota_left = total_quota - quota_used
                
                total = math.floor(total_quota/3600)
                used = math.floor(quota_used/3600)
                hours = math.floor(quota_left/3600)
                minutes = math.floor(quota_left/60 % 60)
                days = math.floor(hours/24)

                usedperc = math.floor(quota_used / total_quota * 100)
                leftperc = math.floor(quota_left / total_quota * 100)

                quota_details = f"""
**Heroku Account Status**
▪️ 𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 {total} нσυяѕ 𝐨𝐟 𝐟𝐫𝐞𝐞 𝐝𝐲𝐧𝐨𝐬 𝐚𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐞𝐚𝐜𝐡 𝐦𝐨𝐧𝐭𝐡.
▫️ 𝐃𝐲𝐧𝐨 𝐡𝐨𝐮𝐫𝐬 𝐮𝐬𝐞𝐝 𝐭𝐡𝐢𝐬 𝐦𝐨𝐧𝐭𝐡:- {used} нσυяѕ ( {usedperc}% )
▫️ 𝐃𝐲𝐧𝐨 𝐡𝐨𝐮𝐫𝐬 𝐫𝐞𝐦𝐚𝐢𝐧𝐢𝐧𝐠 𝐭𝐡𝐢𝐬 𝐦𝐨𝐧𝐭𝐡:
        - {hours} нσυяѕ ( {leftperc}% )
        - αρρяσχ {days} 𝐃𝐚𝐲𝐬!
"""
            else:
                quota_details = ""
        except:
            print("Check your Heroku API key")
            quota_details = ""
    else:
        quota_details = ""

    uptime = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - BOT_START_TIME))

    try:
        t, u, f = shutil.disk_usage(".")
        total = humanbytes(t)
        used = humanbytes(u)
        free = humanbytes(f)

        disk = "\n**Disk Details**\n\n" \
            f"▪️ 𝐔𝐬𝐞𝐝  :  {used} / {total}\n" \
            f"▫️ 𝐅𝐫𝐞𝐞  :  {free}\n\n"
    except:
        disk = ""

    await message.reply_text(
        "**⚙️ Current status of your bot ⚙️!**\n"
        f"▫️ **Used in** **{chats}** **chats**\n\n"
        f"▫️BOT Uptime : **{uptime}**\n\n"
        f"{quota_details}"
        f"{disk}",
        quote=True,
        parse_mode="md"
    )

@Client.on_message(filters.private & filters.command('admincmd'))
async def admincmd(bot, message):
    admin_cmd_text="""
𝐇𝐞𝐫𝐞 𝐚𝐫𝐞 𝐭𝐡𝐞 𝐁𝐨𝐭 𝐀𝐝𝐦𝐢𝐧 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:

▫️/index - 𝐓𝐨 𝐢𝐧𝐝𝐞𝐱 𝐚𝐥𝐥 𝐅𝐢𝐥𝐞𝐬 𝐟𝐫𝐨𝐦 𝐚 𝐂𝐡𝐚𝐧𝐧𝐞𝐥.
▫️/channel - 𝐆𝐞𝐭 𝐛𝐚𝐬𝐢𝐜 𝐢𝐧𝐟𝐨𝐦𝐚𝐭𝐢𝐨𝐧 𝐚𝐛𝐨𝐮𝐭 𝐂𝐡𝐚𝐧𝐧𝐞𝐥𝐬.
▫️/total - 𝐒𝐡𝐨𝐰 𝐭𝐨𝐭𝐚𝐥 𝐨𝐟 𝐬𝐚𝐯𝐞𝐝 𝐟𝐢𝐥𝐞𝐬.
▫️/delete - 𝐃𝐞𝐥𝐞𝐭𝐞 𝐟𝐢𝐥𝐞 𝐟𝐫𝐨𝐦 𝐝𝐚𝐭𝐚𝐛𝐚𝐬𝐞.
▫️/logger - 𝐆𝐞𝐭 𝐥𝐨𝐠 𝐟𝐢𝐥𝐞.
"""
    await message.reply(
        text=admin_cmd_text,
        reply_markup=InlineKeyboardMarkup(
            [
                InlineKeyboardButton('❌ Close', callback_data="close_data"),
                InlineKeyboardButton('👤 About', callback_data="about")
            ]
        ),
        disable_web_page_preview=True,
        reply_to_message_id=message.from_user.id
    ) 
