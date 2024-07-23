from DEVINE import DEVINE
from pyrogram import filters
from config import OWNER_ID

# Define a handler for the /viewlogs command
@DEVINE.on_message(filters.private & filters.command("viewlogs"))
def view_logs_command(client, message):
    user_id = message.from_user.id
    
    # Check if the user is the owner
    if user_id not in OWNER_ID:
        message.reply("You are not authorized to use this command.")
        return
    
    # Read the log file
    try:
        with open('bot.log', 'r') as log_file:
            logs = log_file.read()
            if logs:
                message.reply(f"Here are the latest logs:\n\n{logs}")
            else:
                message.reply("The log file is empty.")
    except FileNotFoundError:
        message.reply("Log file not found.")
