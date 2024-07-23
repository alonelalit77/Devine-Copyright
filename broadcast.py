from DEVINE import DEVINE
from pyrogram import filters
from config import OWNER_ID

@DEVINE.on_message(filters.private & filters.command("broadcast") & filters.user(OWNER_ID))
def broadcast(client, message):
    # Extract the broadcast message
    broadcast_message = " ".join(message.text.split()[1:])
    if not broadcast_message:
        message.reply("Please provide a message to broadcast.")
        return

    # Send the broadcast message to all groups and supergroups
    dialogs = client.get_dialogs()
    for dialog in dialogs:
        if dialog.chat.type in ["group", "supergroup"]:
            client.send_message(dialog.chat.id, broadcast_message)
    
    message.reply("Broadcast message sent!")
