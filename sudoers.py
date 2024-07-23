# sudoers.py

from DEVINE import DEVINE
from pyrogram import filters
from config import OWNER_ID

# In-memory store for sudoers
sudoers = set()

def add_sudo(user_id):
    """Add a user to the sudoers list."""
    sudoers.add(user_id)
    return f"User {user_id} added to sudoers."

def remove_sudo(user_id):
    """Remove a user from the sudoers list."""
    if user_id in sudoers:
        sudoers.remove(user_id)
        return f"User {user_id} removed from sudoers."
    return f"User {user_id} is not in sudoers."

def check_sudo(user_id):
    """Check if a user is a sudoer."""
    return user_id in sudoers

def list_sudoers():
    """List all sudoers."""
    return list(sudoers)

@DEVINE.on_message(filters.private & filters.command(["addsudo", "delsudo", "sudoers"]))
def sudo_command(client, message):
    if message.from_user.id not in OWNER_ID:
        message.reply("You are not authorized to use this command.")
        return

    command = message.text.split()[0]
    if command == "/addsudo":
        if len(message.text.split()) < 2:
            message.reply("Please provide the user ID to add.")
            return
        try:
            user_id = int(message.text.split()[1])
        except ValueError:
            message.reply("Invalid user ID format.")
            return
        result = add_sudo(user_id)
        message.reply(result)
    elif command == "/delsudo":
        if len(message.text.split()) < 2:
            message.reply("Please provide the user ID to remove.")
            return
        try:
            user_id = int(message.text.split()[1])
        except ValueError:
            message.reply("Invalid user ID format.")
            return
        result = remove_sudo(user_id)
        message.reply(result)
    elif command == "/sudoers":
        sudo_list = list_sudoers()
        if sudo_list:
            message.reply(f"Sudoers list: {', '.join(map(str, sudo_list))}")
        else:
            message.reply("No sudoers in the list.")
