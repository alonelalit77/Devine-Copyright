from pyrogram import Client, filters
from DEVINE import DEVINE
import sudoers
import broadcast
import re

# Define a list of keywords or phrases that indicate copyrighted material
copyright_keywords = [
    "copyrighted",
    "pirated",
    "illegal",
    "torrent",
    "download",
    "free movie",
    "free music",
    "free software"
]

# Track user violations
user_violations = {}

# Define a list of admin user IDs (replace with actual admin IDs)
admins = [123456789, 987654321]  # Replace with actual admin user IDs

# Define a function to check for copyrighted material
def is_copyrighted_message(message_text):
    for keyword in copyright_keywords:
        if re.search(keyword, message_text, re.IGNORECASE):
            return True
    return False

# Define a function to check if the bot has the necessary permissions
def has_permissions(client, chat_id):
    chat_member = client.get_chat_member(chat_id, client.get_me().id)
    return (chat_member.can_change_info and 
            chat_member.can_delete_messages and 
            chat_member.can_restrict_members and 
            chat_member.can_promote_members)

# Define a function to promote a user to admin
def promote_to_admin(client, chat_id, user_id):
    if not has_permissions(client, chat_id):
        client.send_message(chat_id, "⚠️ The bot lacks some necessary permissions. Please grant the following permissions:\n"
                                      "- Change Group Info\n"
                                      "- Delete Messages\n"
                                      "- Ban Users\n"
                                      "- Add New Admins")
        return

    client.promote_chat_member(
        chat_id,
        user_id,
        can_change_info=True,
        can_delete_messages=True,
        can_invite_to_group=True,
        can_pin_messages=True,
        can_restrict_members=True,
        can_promote_members=True
    )
    client.send_message(chat_id, f"✅ User {user_id} has been promoted to admin.")

# Define a function to demote a user from admin
def demote_from_admin(client, chat_id, user_id):
    if not has_permissions(client, chat_id):
        client.send_message(chat_id, "⚠️ The bot lacks some necessary permissions. Please grant the following permissions:\n"
                                      "- Change Group Info\n"
                                      "- Delete Messages\n"
                                      "- Ban Users\n"
                                      "- Add New Admins")
        return

    client.promote_chat_member(
        chat_id,
        user_id,
        can_change_info=False,
        can_delete_messages=False,
        can_invite_to_group=False,
        can_pin_messages=False,
        can_restrict_members=False,
        can_promote_members=False
    )
    client.send_message(chat_id, f"❌ User {user_id} has been demoted from admin.")

# Define a handler for new messages
@DEVINE.on_message(filters.group & filters.text)
def check_copyright(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check if the bot has required permissions
    if not has_permissions(client, chat_id):
        client.send_message(chat_id, "⚠️ The bot lacks some necessary permissions. Please grant the following permissions:\n"
                                      "- Change Group Info\n"
                                      "- Delete Messages\n"
                                      "- Ban Users\n"
                                      "- Add New Admins")
        return

    # Handle potential copyright issues differently for admins
    if is_copyrighted_message(message.text):
        if message.from_user.id in admins:
            client.send_message(chat_id, f"⚠️ Warning: The message from {message.from_user.first_name} may contain copyrighted material.")
        else:
            # Delete the message if it's not from an admin
            message.delete()

            # Increment the user's violation count
            if user_id not in user_violations:
                user_violations[user_id] = 1
            else:
                user_violations[user_id] += 1

            # Send a warning message to the group
            client.send_message(chat_id, f"⚠️ A message containing potentially copyrighted material was deleted. User {message.from_user.first_name} has violated the rules {user_violations[user_id]} times.")
            
            # Ban the user if they reach 3 violations
            if user_violations[user_id] >= 3:
                client.kick_chat_member(chat_id, user_id)
                client.send_message(chat_id, f"🚫 User {message.from_user.first_name} has been banned for repeated violations.")

# Define a handler for when the bot is added to the group
@DEVINE.on_chat_member_added()
def on_chat_member_added(client, message):
    chat_id = message.chat.id
    
    # Check if the bot was added and has necessary permissions
    if message.new_chat_member.id == client.get_me().id:
        if not has_permissions(client, chat_id):
            client.send_message(chat_id, "⚠️ The bot was added but lacks some necessary permissions. Please grant the following permissions:\n"
                                          "- Change Group Info\n"
                                          "- Delete Messages\n"
                                          "- Ban Users\n"
                                          "- Add New Admins")

# Define a handler for admin promotion commands
@DEVINE.on_message(filters.group & filters.command("promote") & filters.user(admins))
def promote_user(client, message):
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id if message.reply_to_message else None
    
    if not user_id:
        client.send_message(chat_id, "❗ Please reply to the user you want to promote.")
        return
    
    promote_to_admin(client, chat_id, user_id)

# Define a handler for admin demotion commands
@DEVINE.on_message(filters.group & filters.command("demote") & filters.user(admins))
def demote_user(client, message):
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id if message.reply_to_message else None
    
    if not user_id:
        client.send_message(chat_id, "❗ Please reply to the user you want to demote.")
        return
    
    demote_from_admin(client, chat_id, user_id)

# Start the bot
DEVINE.run()
