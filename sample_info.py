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
**If you want to Set me up in your Group, Just Add me to your Group & Make Me an Admin.**
**I will respond to the Queries in your Group with Files 🗃️ in my Database.**

**While Requesting for Files in the Group always remeber to Type in the Exact Movie-Name (`copy_paste from Google`).**

Use **🔍 Search Here** to search for Files 🗃️ **Inline**.
"""

MAL_HELP_TXT = """
**നിങ്ങളുടെ ഗ്രൂപ്പിൽ എന്നെ സജ്ജമാക്കാൻ നിങ്ങൾ ആഗ്രഹിക്കുന്നുവെങ്കിൽ, എന്നെ നിങ്ങളുടെ ഗ്രൂപ്പിലേക്ക് ചേർത്ത് എന്നെ ഒരു അഡ്മിൻ ആക്കുക. **
**എന്റെ ഡാറ്റാബേസിലെ ഫയലുകൾ ഉപയോഗിച്ച് നിങ്ങളുടെ ഗ്രൂപ്പിലെ അന്വേഷണങ്ങളോട് ഞാൻ പ്രതികരിക്കും. **

**ഗ്രൂപ്പിലെ ഫയലുകൾക്കായി അഭ്യർത്ഥിക്കുമ്പോൾ എല്ലായ്പ്പോഴും കൃത്യമായ മൂവി-പേര് ടൈപ്പ് ചെയ്യാൻ ഓർമ്മിക്കുക (`GOOGLE ൽ നിന്ന് Copy-Paste ചെയ്യുക`).**
 
ഫയലുകൾ തിരയാൻ **🔍 Search Here** എന്ന **OPTION** ഉപയോഗിക്കുക.
"""
