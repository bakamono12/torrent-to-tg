import os
import pyrogram
import logging
from pyrogram import enums
from pyrogram.errors import MediaEmpty
import requests

from movie_poster import get_poster
from search_engine import generate_url
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# header level stuff for api
logging.getLogger("pyrogram").setLevel(logging.WARNING)
# start the bot with the greeting message admin only access
bot_token = os.environ.get('bot_token')
app = pyrogram.Client("bot_token", bot_token=bot_token)


def admin_only(func):
    async def wrapper(client, message):
        if message.from_user.id in [852259634, 5487058679]:
            await func(client, message)
        else:
            await client.send_photo(photo='./img/CoSxK.jpg',
                                    has_spoiler=True,
                                    chat_id=message.chat.id,
                                    reply_to_message_id=message.id
                                    )

    return wrapper


# chat action for uploading photo
async def send_uploading_action(client, chat_id):
    await client.send_chat_action(chat_id, enums.ChatAction.UPLOAD_PHOTO)


# chat action for typing
async def send_typing_action(client, chat_id):
    await client.send_chat_action(chat_id, enums.ChatAction.TYPING)


# start command handler
@app.on_message(pyrogram.filters.command("start"))
@admin_only
async def start_command_handler(client, message):
    # Display the initial video and buttons
    bot_message = await client.send_message(message.chat.id,
                                            "Welcome to The Torrent To TG Bot use /search {query} to get started.,"
                                            "This bot is made by @DTMK_C",
                                            reply_to_message_id=message.id)


# Maintain a dictionary to store user-specific data, including the current position in the list
user_data = {}


@app.on_message(pyrogram.filters.command("search"))
@admin_only
async def search_command_handler(client, message):
    # send request to the search engine and get the results
    query = message.text.split()
    if len(query) > 1:
        query = " ".join(query[1:])
        poster = get_poster(query)
        await send_typing_action(client, message.chat.id)
        results = generate_url(query)
        print(results)
        if results:
            # Initialize the user-specific data when sending the first message
            user_data[message.from_user.id] = {
                "results": results,
                "current_index": 0
            }
            await send_uploading_action(client, message.chat.id)
            await send_result_message(client, message, message.chat.id, poster, query, 0)
    else:
        await client.send_message(
            message.chat.id,
            "Please enter a search query.",
            reply_to_message_id=message.message_id
        )


# Helper function to send the result message with inline buttons
async def send_result_message(client, message, chat_id, poster, query, current_index):
    results = user_data[message.from_user.id]["results"]
    result = results[current_index]

    # Create the inline keyboard with "Next" and "Download" buttons
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text="Next",
                callback_data="next"
            ),
            InlineKeyboardButton(
                text="Download",
                callback_data="download"
            )
        ]
    ]

    # Add "Prev" button if current_index is greater than 0
    if current_index > 0:
        inline_keyboard[0].insert(0, InlineKeyboardButton(
            text="Previous",
            callback_data="prev"
        ))
    try:
        await client.send_photo(
            chat_id,
            photo=poster if poster else "./img/not_found.png",
            caption=f"Name: {result['name']}\n\n🟢 Seeders: {result['seeder']} |🔴 Leechers: {result['leecher']}\n🎥 Size: "
                    f"{result['size']}\n⬆️ Uploaded: {result['age']} ago!\n🔞 NSFW: { '✅' if result['nsfw'] else '❌'}\n",
            reply_markup=InlineKeyboardMarkup(inline_keyboard),
            reply_to_message_id=message.id,
        )
    except MediaEmpty:
        download_image = requests.get(poster)
        with open('./img/poster.jpg', 'wb') as f:
            f.write(download_image.content)
        await client.send_photo(
            chat_id,
            photo="./img/poster.jpg",
            caption=f"Name: {result['name']}\n\n🟢 Seeders: {result['seeder']} |🔴 Leechers: {result['leecher']}\n🎥 Size: "
                    f"{result['size']}\n⬆️ Uploaded: {result['age']} ago!\n🔞 NSFW: { '✅' if result['nsfw'] else '❌'}\n",
            reply_markup=InlineKeyboardMarkup(inline_keyboard),
            reply_to_message_id=message.id,
        )
        os.remove('./img/poster.jpg')
    except Exception as e:
        await client.send_message(text="Some Error Occured Try Again !\nError info: " + str(e),
                                  chat_id=chat_id,
                                  reply_to_message_id=message.id)


# Handle callback queries
@app.on_callback_query()
async def handle_callback_query(client, callback_query):
    query_data = callback_query.data
    user_id = callback_query.from_user.id

    # Check if the user's data exists in the dictionary
    if user_id in user_data:
        current_index = user_data[user_id]["current_index"]

        # Move the current index based on the callback data
        if query_data == "next":
            current_index = min(current_index + 1, len(user_data[user_id]["results"]) - 1)
        elif query_data == "prev":
            current_index = max(current_index - 1, 0)

        user_data[user_id]["current_index"] = current_index

        results = user_data[user_id]["results"]
        result = results[current_index]

        # Create the inline keyboard with "Next" and "Download" buttons
        inline_keyboard = [
            [
                InlineKeyboardButton(
                    text="Next",
                    callback_data="next"
                ),
                InlineKeyboardButton(
                    text="Download",
                    callback_data="download"
                )
            ]
        ]

        # Add "Prev" button if current_index is greater than 0
        if current_index > 0:
            inline_keyboard[0].insert(0, InlineKeyboardButton(
                text="Previous",
                callback_data="prev"
            ))

        # Send the updated result message
        await callback_query.message.edit_caption(
            caption=f"Name: {result['name']}\n\n🟢 Seeders: {result['seeder']} |🔴 Leechers: {result['leecher']}\n🎥 Size: "
                    f"{result['size']}\n⬆️ Uploaded: {result['age']} ago!\n🔞 NSFW: { '✅ - Yes' if result['nsfw'] else '❌- NO'}\n",
            reply_markup=InlineKeyboardMarkup(inline_keyboard)
        )

        # Answer the callback query to remove the "waiting" status
        await callback_query.answer()
    else:
        # Handle the case if the user data doesn't exist in the dictionary (possibly due to bot restart)
        await callback_query.answer("Your session has expired. Please search again.")


app.run()
