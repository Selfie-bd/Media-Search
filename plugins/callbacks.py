import os
import ast

from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

if bool(os.environ.get("WEBHOOK", False)):
    from info import 
else:
    from info import 


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
async def cb_handler_2(client, qry):

 
    if qry.data == "delallconfirm":
        userid = qry.from_user.id
        chat_type = qry.message.chat.type

        if chat_type == "private":
            grpid  = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await qry.message.edit_text("Make sure I'm present in your group!!", quote=True)
                    return
            else:
                await qry.message.edit_text(
                    "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                    quote=True
                )
                return

        elif (chat_type == "group") or (chat_type == "supergroup"):
            grp_id = qry.message.chat.id
            title = qry.message.chat.title

        else:
            return

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == "creator") or (str(userid) in AUTH_USERS_2):    
            await del_all(qry.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!",show_alert=True)
    
    elif qry.data == "delallcancel":
        userid = qry.from_user.id
        chat_type = qry.message.chat.type
        
        if chat_type == "private":
            await qry.message.reply_to_message.delete()
            await qry.message.delete()

        elif (chat_type == "group") or (chat_type == "supergroup"):
            grp_id = qry.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == "creator") or (str(userid) in AUTH_USERS_2):
                await qry.message.delete()
                try:
                    await qry.message.reply_to_message.delete()
                except:
                    pass
            else:
                await qry.answer("Thats not for you!!",show_alert=True)


    elif "groupcb" in qry.data:
        await qry.answer()

        group_id = qry.data.split(":")[1]
        title = qry.data.split(":")[2]
        act = qry.data.split(":")[3]
        user_id = qry.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}:{title}"),
                InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await qry.message.edit_text(
            f"Group Name : **{title}**\nGroup ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode="md"
        )
        return

    elif "connectcb" in qry.data:
        await qry.answer()

        group_id = qry.data.split(":")[1]
        title = qry.data.split(":")[2]
        user_id = qry.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await qry.message.edit_text(
                f"Connected to **{title}**",
                parse_mode="md"
            )
            return
        else:
            await qry.message.edit_text(
                f"Some error occured!!",
                parse_mode="md"
            )
            return

    elif "disconnect" in qry.data:
        await qry.answer()

        title = qry.data.split(":")[2]
        user_id = qry.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await qry.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode="md"
            )
            return
        else:
            await qry.message.edit_text(
                f"Some error occured!!",
                parse_mode="md"
            )
            return
    elif "deletecb" in qry.data:
        await qry.answer()

        user_id = qry.from_user.id
        group_id = qry.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await qry.message.edit_text(
                "Successfully deleted connection"
            )
            return
        else:
            await qry.message.edit_text(
                f"Some error occured!!",
                parse_mode="md"
            )
            return
    
    elif qry.data == "backcb":
        await qry.answer()

        userid = qry.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await qry.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                if active:
                    act = " - ACTIVE"
                else:
                    act = ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{title}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await qry.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

    elif "alertmessage" in qry.data:
        grp_id = qry.message.chat.id
        i = qry.data.split(":")[1]
        keyword = qry.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await qry.answer(alert,show_alert=True)
