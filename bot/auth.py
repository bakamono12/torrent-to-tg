from pyrogram import Client


def create_session():
    api_id = int(input("Enter your API ID: "))
    api_hash = input("Enter your API HASH: ")
    bot_token = input("Enter Your Bot Token: ")

    client = Client(
        "my_bot_session",
        api_id=api_id,
        api_hash=api_hash,
        bot_token=bot_token
    )

    return client


if __name__ == "__main__":
    app = create_session()
    app.run()
