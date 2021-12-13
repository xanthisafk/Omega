from time import sleep
import codecs
import json
def main():

    print()
    print("Welcome to Omega setup.")
    print("Thank you for downloading Omega.")
    print("This setup will guide you through the initial setup of bot.")
    print()

    input("Press enter to continue. ")
    print()
    name = input("Enter bot's name: ")
    prefix = input("Choose a prefix: ")
    secret = input("Enter the bot secret: ")
    while True:
        try:
            owner = int(input("Enter ID of owner: "))
            break
        except Exception as e:
            if isinstance(e, ValueError):
                print("ID must be a number.")


    emotes = "# Emotes\nEMOTE_LEFT = '⬅'\nEMOTE_RIGHT = '➡'\nEMOTE_OK = '🆗'\nEMOTE_ERROR = '❌'\nEMOTE_UPVOTE = '⬆'\nEMOTE_DOWNVOTE = '⬇'\nEMOTE_WARNING = '⚠'\nEMOTE_ZERO = '0️⃣'\nEMOTE_ONE = '1️⃣'\nEMOTE_TWO = '2️⃣'\nEMOTE_THREE = '3️⃣'\nEMOTE_FOUR = '4️⃣'\nEMOTE_FIVE = '5️⃣'\nEMOTE_SIX = '6️⃣'\n\n"

    print()

    db = input("Do you have a Redis database setup?\nIf not, setup your Redis database using a free account on: https://redis.com/try-free\n (y/n): ")

    if db == 'n':
        s2 = """
Please setup a Redis database. Without it, ATKs won't work.
You can Google for instructions.
I suggest you use 'https://redis.com/try-free/' and sign up for a free tier.
        """
        print(s2)
        print("Exiting...")
        exit()
    else:
        db_host = input("Enter database host: ")
        while True:
            try:
                db_port = input("Enter database port: ")
                break
            except ValueError:
                print("Port must be a number.")


        db_pass = input("Enter database pass: ")

    
    db = input("Do you have a debug channel where the bot can send logs? (y/n): ")
    if db == 'y':
        while True:
            try:
                channel = int(input("Enter channel ID: "))
                break
            except Exception as e:
                if isinstance(e, ValueError):
                    print("ID must be a number.\n")

    db = input("Do you have a support server where people can contact you for support? (y/n): ")
    if db == 'y':
        while True:
            try:
                guild = int(input("Enter guild ID: "))
                break
            except Exception as e:
                if isinstance(e, ValueError):
                    print("ID must be a number.\n")
    else:
        pass

    yes = input("Do you have a Reddit application ready?\nIf not, create on for free on 'https://reddit.com/prefs/apps'\nI prefer you use a throwaway account for this.\n(y/n): ")
    if yes == 'y':
        reddit_id = input("Enter client ID: ")
        reddit_secret = input("Enter client secret: ")
        print("I recommend that you create a new account just to use with this bot.")
        reddit_user = input("Enter username: ")
        reddit_pass = input("Enter password: ")

    else:
        print("\nYou may experience increased amount of errors while using `GET` or `MEME` commands.\n")
        reddit_id = None
        reddit_secret = None
        reddit_user = None
        reddit_pass = None

    data = {
        "general":{
            "NAME": name,
            "PREFIX": prefix,
            "TOKEN": secret,
            "OWNER": owner,
            "GUILD": guild
        },
        
        "emotes":{
            "LEFT": "⬅",
            "RIGHT": "➡",
            "OK": "🆗",
            "ERROR": "❌",
            "UPVOTE": "⬆",
            "DOWNVOTE": "⬇",
            "WARNING": "⚠",
            "ZERO": "0️⃣",
            "ONE": "1️⃣",
            "TWO": "2️⃣",
            "THREE": "3️⃣",
            "FOUR": "4️⃣",
            "FIVE": "5️⃣",
            "SIX": "6️⃣"
        },

        "debug":{
            "CHANNEL": channel
        },

        "redis":{
            "HOST": db_host,
            "PORT": db_port,
            "PASS": db_pass
        },

        "reddit":{
            "ID": reddit_id,
            "SECRET": reddit_secret,
            "USER": reddit_user,
            "PASS": reddit_pass
        }
    }

    with codecs.open('config.py', 'w',encoding='utf-8') as f:
        data = json.dumps(data,indent=4)
        f.write(data)

    s3 = """
The bot is now set-up. You can start it by typing:
"python main.py"
You can also always change the config.py file to change these settings.
Thank you for using Omega!
    """
    print(s3)
    sleep(5)

if __name__ == '__main__':
    main()

