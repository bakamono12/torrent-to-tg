from pyrogram import Client

app = Client(
    "bot_token",
    api_id=input("Enter your API ID: "),
    api_hash=input("Enter your API HASH: "),
    bot_token=input("Enter Your Bot Token: "))

if __name__ == "__main__":
    app.run()
