import os
import pymongo

if bool(os.environ.get("WEBHOOK", False)):
    from info import DATABASE_URI, DATABASE_NAME_2
else:
    from info import DATABASE_URI, DATABASE_NAME_2
 
myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME_2]
mycol = mydb['USERS']



async def add_user(id, username, name, dcid):
    data = {
        '_id': id,
        'username' : username,
        'name' : name,
        'dc_id' : dcid
    }
    try:
        mycol.update_one({'_id': id},  {"$set": data}, upsert=True)
    except:
        pass


async def all_users():
    count = mycol.count()
    return count


async def find_user(id):
    query = mycol.find( {"_id":id})

    try:
        for file in query:
            name = file['name']
            username = file['username']
            dc_id = file['dc_id']
        return name, username, dc_id
    except:
        return None, None, None
