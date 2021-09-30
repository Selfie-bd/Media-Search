# Bot information
SESSION = 'Media_search'
USER_SESSION = 'User_Bot'
API_ID = 12345
API_HASH = '0123456789abcdef0123456789abcdef'
BOT_TOKEN = '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'
USERBOT_STRING_SESSION = ''

# Bot settings
CACHE_TIME = 300
USE_CAPTION_FILTER = False

# Admins, Channels & Users
ADMINS = [12345789, 'admin123', 98765432]
CHANNELS = [-10012345678, -100987654321, 'channelusername']
AUTH_USERS = []
AUTH_CHANNEL = None

# MongoDB information
DATABASE_URI = "mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb]?retryWrites=true&w=majority"
DATABASE_NAME = 'Telegram'
COLLECTION_NAME = 'channel_files'  # If you are using the same database, then use different collection name for each bot

# Messages
START_MSG = """
**Hi, I'm Media bot**

Here you can search files in inline mode. Just press follwing buttons and start searching.
"""

SHARE_BUTTON_TEXT = 'Checkout {username} for searching files'
INVITE_MSG = 'Please join @.... to use this bot'

HELP_TEXT = """
• I am usable both in **PM** & in **Groups** ✨.

 • In **PM** 🗣️: You can access files by just typing the 🎞️ **Movie/Series** name in my **PM** and also via **INLINE**.

 • In **GROUP** 🗣️: You have to Add ➕ me to a **GROUP** and make me an **ADMIN** 🤴. I will respond to the Queries Accordingly.

 • **/reqformat**: Use this **COMMAND** to get the Request Format. Requests of this kind is likely to get more accurate **RESULTS** ✨.

**© @PrimeFlixMedia_All 📍**
"""

MAL_HELP_TXT = """
നിങ്ങളുടെ ഗ്രൂപ്പിൽ എന്നെ സജ്ജമാക്കാൻ നിങ്ങൾ ആഗ്രഹിക്കുന്നുവെങ്കിൽ, എന്നെ നിങ്ങളുടെ ഗ്രൂപ്പിലേക്ക് ചേർത്ത് എന്നെ ഒരു അഡ്മിൻ ആക്കുക. 
എന്റെ ഡാറ്റാബേസിലെ ഫയലുകൾ 🗃️ ഉപയോഗിച്ച് നിങ്ങളുടെ ഗ്രൂപ്പിലെ അന്വേഷണങ്ങളോട് ഞാൻ പ്രതികരിക്കും. 

ഗ്രൂപ്പിലെ ഫയലുകൾക്കായി അഭ്യർത്ഥിക്കുമ്പോൾ എല്ലായ്പ്പോഴും കൃത്യമായ മൂവി-പേര് ടൈപ്പ് ചെയ്യാൻ ഓർമ്മിക്കുക (`GOOGLE ൽ നിന്ന് Copy-Paste ചെയ്യുക`).
 
ഫയലുകൾ തിരയാൻ **🔍 Search Here** എന്ന **OPTION** ഉപയോഗിക്കുക.
"""

HELP_MSG = """
•Add ~ мє αѕ αη 𝗔𝗗𝗠𝗜𝗡 & ѕтαят Filtering..😉
𝗕𝗔𝗦𝗜𝗖 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦:
/start - ᴄʜᴇᴄᴋ ɪғ ɪ'ᴍ ᴀʟɪᴠᴇ!!
/help - ᴄᴏᴍᴍᴀɴᴅ ʜᴇʟᴘ!
/about - ᴍʏ ᴅᴇᴛᴀɪʟs
𝗙𝗜𝗟𝗧𝗘𝗥 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦:
•/add name reply -  Add filter for name
•/del name -  Delete filter
•/delall -  Delete entire filters (Group Owner Only!)
•/viewfilters -  List all filters in chat
<b𝗖𝗢𝗡𝗡𝗘𝗖𝗧𝗜𝗢𝗡 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦:</b>
<code>/connect groupid</code>  -  Connect your group to my PM. You can also simply use,
<code>/connect</code> in groups.
<code>/connections</code>  -  Manage your connections.
<b>𝗘𝗫𝗧𝗥𝗔𝗦:</b>
/status  -  Shows current status of your bot (Auth User Only)
/id  -  Shows ID information
/info userid -  Shows User Information. Use <code>/info</code> as reply to some message for their details!
♻🄿🄾🅆🄴🅁🄴🄳 🄱🅈: <b>@PrimeFlixMedia_All</b>
"""
