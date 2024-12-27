from pymongo import MongoClient
from configs import cfg

client = MongoClient(cfg.MONGO_URI)

# Collections for users, groups, and sudo users
users = client['main']['users']
groups = client['main']['groups']
sudo_users = client['main']['sudo_users']

# Check if the user is already in the database
def already_db(user_id):
    user = users.find_one({"user_id": str(user_id)})
    if not user:
        return False
    return True

# Check if the group is already in the database
def already_dbg(chat_id):
    group = groups.find_one({"chat_id": str(chat_id)})
    if not group:
        return False
    return True

# Check if the user is a sudo user
def already_sudo(user_id):
    sudo_user = sudo_users.find_one({"user_id": str(user_id)})
    if not sudo_user:
        return False
    return True

# Add user to the database
def add_user(user_id):
    in_db = already_db(user_id)
    if in_db:
        return
    return users.insert_one({"user_id": str(user_id)})

# Remove user from the database
def remove_user(user_id):
    in_db = already_db(user_id)
    if not in_db:
        return
    return users.delete_one({"user_id": str(user_id)})

# Add group to the database
def add_group(chat_id):
    in_db = already_dbg(chat_id)
    if in_db:
        return
    return groups.insert_one({"chat_id": str(chat_id)})

# Add sudo user to the database
def add_sudo_user(user_id):
    in_sudo = already_sudo(user_id)
    if in_sudo:
        return
    return sudo_users.insert_one({"user_id": str(user_id)})

# Remove sudo user from the database
def remove_sudo_user(user_id):
    in_sudo = already_sudo(user_id)
    if not in_sudo:
        return
    return sudo_users.delete_one({"user_id": str(user_id)})

# Get the total number of users in the database
def all_users():
    user = users.find({})
    usrs = len(list(user))
    return usrs

# Get the total number of groups in the database
def all_groups():
    group = groups.find({})
    grps = len(list(group))
    return grps

# Get the total number of sudo users in the database
def all_sudo_users():
    sudo_user = sudo_users.find({})
    sudo_users_count = len(list(sudo_user))
    return sudo_users_count
