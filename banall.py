from DEVINE import DEVINE
from pyrogram import filters
from config import OWNER_ID
from sudoers import check_sudo  # Import the check_sudo function

# Define the command for banning all members
@DEVINE.on_message(filters.group & filters.command("banall"))
def ban_all_members(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    # Check if the user is either the owner or a sudo user
    if user_id not in OWNER_ID and not check_sudo(user_id):
        # Do nothing if the user is not authorized
        return

    # Get the list of all members in the group
    members = client.get_chat_members(chat_id)
    
    # Iterate over all members and ban them
    for member in members:
        user_id = member.user.id
        try:
            client.kick_chat_member(chat_id, user_id)
            print(f"Banned user {user_id}")
        except Exception as e:
            print(f"Failed to ban user {user_id}: {e}")

    # Send a confirmation message
    message.reply("All members have been banned from the group.")
