import os
import re
import pymongo

if bool(os.environ.get("WEBHOOK", False)):
    from info import Config
else:
    from info import Config
 
myclient = pymongo.MongoClient(Config.DATABASE_URI_2)
mydb = myclient[Config.DATABASE_NAME_2]



async def add_filter(grp_id, text, reply_text, btn, file, alert):
    mycol = mydb[str(grp_id)]
    # mycol.create_index([('text', 'text')])

    data = {
        'text':str(text),
        'reply':str(reply_text),
        'btn':str(btn),
        'file':str(file),
        'alert':str(alert)
    }

    try:
        mycol.update_one({'text': str(text)},  {"$set": data}, upsert=True)
    except:
        print('Couldnt save, check your db')
             
     
async def find_filter(group_id, name):
    mycol = mydb[str(group_id)]
    
    query = mycol.find( {"text":name})
    # query = mycol.find( { "$text": {"$search": name}})
    try:
        for file in query:
            reply_text = file['reply']
            btn = file['btn']
            fileid = file['file']
            try:
                alert = file['alert']
            except:
                alert = None
        return reply_text, btn, alert, fileid
    except:
        return None, None, None, None


async def get_filters(group_id):
    mycol = mydb[str(group_id)]

    texts = []
    query = mycol.find()
    try:
        for file in query:
            text = file['text']
            texts.append(text)
    except:
        pass
    return texts


async def delete_filter(message, text, group_id):
    mycol = mydb[str(group_id)]
    
    myquery = {'text':text }
    query = mycol.count_documents(myquery)
    if query == 1:
        mycol.delete_one(myquery)
        await message.reply_text(
            f"🌩️'`{text}`' 𝐝𝐞𝐥𝐞𝐭𝐞𝐝. 𝐈'𝐥𝐥 𝐧𝐨𝐭 𝐫𝐞𝐬𝐩𝐨𝐧𝐝 𝐭𝐨 𝐭𝐡𝐚𝐭 𝐟𝐢𝐥𝐭𝐞𝐫 𝐚𝐧𝐲𝐦𝐨𝐫𝐞.",
            quote=True,
            parse_mode="md"
        )
    else:
        await message.reply_text("𝐂𝐨𝐮𝐥𝐝𝐧'𝐭 𝐟𝐢𝐧𝐝 𝐭𝐡𝐚𝐭 𝐟𝐢𝐥𝐭𝐞𝐫 🥲!", quote=True)


async def del_all(message, group_id, title):
    if str(group_id) not in mydb.list_collection_names():
        await message.edit_text(f"𝐍𝐨𝐭𝐡𝐢𝐧𝐠 𝐭𝐨 𝐫𝐞𝐦𝐨𝐯𝐞 𝐢𝐧 {title}!")
        return
        
    mycol = mydb[str(group_id)]
    try:
        mycol.drop()
        await message.edit_text(f"𝐀𝐥𝐥 𝐟𝐢𝐥𝐭𝐞𝐫𝐬 𝐟𝐫𝐨𝐦 {title} 𝐡𝐚𝐬 𝐛𝐞𝐞𝐧 𝐫𝐞𝐦𝐨𝐯𝐞𝐝 ✅")
    except:
        await message.edit_text(f"𝐂𝐨𝐮𝐥𝐝𝐧'𝐭 𝐫𝐞𝐦𝐨𝐯𝐞 𝐚𝐥𝐥 𝐟𝐢𝐥𝐭𝐞𝐫𝐬 𝐟𝐫𝐨𝐦 𝐠𝐫𝐨𝐮𝐩 🥲!")
        return


async def count_filters(group_id):
    mycol = mydb[str(group_id)]

    count = mycol.count()
    if count == 0:
        return False
    else:
        return count


async def filter_stats():
    collections = mydb.list_collection_names()

    if "CONNECTION" in collections:
        collections.remove("CONNECTION")
    if "USERS" in collections:
        collections.remove("USERS")

    totalcount = 0
    for collection in collections:
        mycol = mydb[collection]
        count = mycol.count()
        totalcount = totalcount + count

    totalcollections = len(collections)

    return totalcollections, totalcount
