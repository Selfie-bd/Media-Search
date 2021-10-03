import os
import ast

from pyrogram import Client as ClaeysBot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

if bool(os.environ.get("WEBHOOK", False)):
    from info import Config
else:
    from info import Config

from database.filters_mdb import del_all, find_filter

from database.connections_mdb import(
    all_connections,
    active_connection,
    if_active,
    delete_connection,
    make_active,
    make_inactive
)
