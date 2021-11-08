from time import sleep
def main():

    s1 = """
Welcome to Omega setup.
Thank you for downloading Omega.
This setup will guide you through the initial setup of bot.
"""

    print(s1)
    input("Press enter to continue. ")

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

    writee = f"# General\nNAME = '{name}'\nPREFIX = ['{prefix}']\nSECRET = '{secret}'\nOWNER = {owner}\n\n"

    writee += "# Emotes\nEMOTE_LEFT = '⬅'\nEMOTE_RIGHT = '➡'\nEMOTE_OK = '🆗'\nEMOTE_ERROR = '❌'\nEMOTE_UPVOTE = '⬆'\nEMOTE_DOWNVOTE = '⬇'\nEMOTE_WARNING = '⚠'\nEMOTE_ZERO = '0️⃣'\nEMOTE_ONE = '1️⃣'\nEMOTE_TWO = '2️⃣'\nEMOTE_THREE = '3️⃣'\nEMOTE_FOUR = '4️⃣'\nEMOTE_FIVE = '5️⃣'\nEMOTE_SIX = '6️⃣'\n\n"

    db = input("Do you have a postgreSQL database setup? (y/n): ")

    if db == 'n':
        s2 = """
Please setup a postgreSQL database. Without it, ATKs won't work.
You can Google for instructions. You can also use ElephantSQL.
        """
        print(s2)
        print("Exiting...")
        exit()
    else:
        db_name = input("Enter database name: ")
        db_host = input("Enter database host: ")
        db_user = input("Enter database user: ")
        db_pass = input("Enter database pass: ")
    
    writee += f"# Database\nDB_HOST = '{db_host}'\nDB_NAME = '{db_name}'\nDB_USER = '{db_user}'\nDB_PASS = '{db_pass}'\n\n"
    
    db = input("Do you have a debug channel & guild where the bot can send logs? (y/n): ")
    if db == 'y':
        while True:
            try:
                channel = int(input("Enter channel ID: "))
                break
            except Exception as e:
                if isinstance(e, ValueError):
                    print("ID must be a number.\n")
        while True:
            try:
                guild = int(input("Enter guild ID: "))
                break
            except Exception as e:
                if isinstance(e, ValueError):
                    print("ID must be a number.\n")


        writee += f"# Debug\nDEBUG = {channel}\nGUILD = {guild}\n"
    else:
        pass

    yes = input("Do you have a Reddit client ready? (y/n): ")
    if yes == 'y':
        reddit_id = input("Enter client ID: ")
        reddit_secret = input("Enter client secret: ")
        writee += f"\n# Reddit\nREDDIT_CLIENT_ID = '{reddit_id}'\nREDDIT_CLIENT_SECRET = {reddit_secret}"
    else:
        writee += "\n# Reddit\nREDDIT_CLIENT_ID = None\nREDDIT_CLIENT_SECRET = None"
        print("\nYou may experience increased amount of errors while using `GET` or `MEME` commands.\n")

    with open('config.py', 'a',encoding='utf-8') as f:
        f.write(writee)
        f.close()
    
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

