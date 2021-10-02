def main():

    s1 = """
    Welcome to Omega setup.
    Thank you for downloading Omega.
    This setup will guide you through the initial setup of bot.

    """

    print(s1)
    input("Press enter to continue. ")

    prefix = input("Choose a prefix: ")
    secret = input("Enter the bot secret: ")
    try:
        owner = int(input("Enter ID of owner: "))
    except Exception as e:
        if isinstance(e, ValueError):
            print("ID must be a number.\nExiting...")
            exit()

    writee = f"# General\nPREFIX = '{prefix}'\nSECRET = '{secret}'\nOWNER = {owner}\n\n"

    db = input("Do you have a postgreSQL database setup? (y/n): ")

    if db == 'n':
        s2 = """
        Please setup a postgreSQL database. Without it, ATKs won't work.
        You can Google for instructions. You can also use ElephantSQL.
        Note: I am trying to make a local doc system. Maybe in v2.
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
    
    db = input("Do you have a debug channel where the bot can send logs? (y/n): ")
    if db == 'y':
        try:
            debug = int(input("Enter channel ID: "))
        except Exception as e:
            if isinstance(e, ValueError):
                print("ID must be a number.\nExiting...")
                exit()

        writee += f"# Debug\nDEBUG = {debug}"
    else:
        pass

    with open('config.py', 'a') as f:
        f.write(writee)
        f.close()
    
    s3 = """
    The bot is now setup. You can start it by typing:
    "python main.py"
    Thank you for using Omega!
    """
    print(s3)

if __name__ == '__main__':
    main()
