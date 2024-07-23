# start.py

from DEVINE import DEVINE
from pyrogram import filters, InlineKeyboardButton, InlineKeyboardMarkup
from config import OWNER_ID

# Define the welcome message with inline buttons
WELCOME_MESSAGE = """
Welcome to the Devine Copyright Protector Bot!

I am here to help manage and protect your group from copyrighted material."""

# Define a handler for the /start command in both DMs and groups
@DEVINE.on_message(filters.command("start"))
def start_command(client, message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    
    # Prepare inline keyboard
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Add me to a group", url="https://t.me/devineXmusic_bot?startgroup=true")],
        [InlineKeyboardButton("Creator", url="tg://openmessage?user_id=6440363814"),
         InlineKeyboardButton("Updates", url="https://t.me/Devine_Network")]
    ])

    # Send the welcome message with the inline keyboard
    client.send_message(
        chat_id,
        f"Hello {user_name}! {WELCOME_MESSAGE}",
        reply_markup=keyboard
  )
