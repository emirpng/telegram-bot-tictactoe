from config import API_TOKEN

from bot.server import bot_server

if __name__ == '__main__':
    if not API_TOKEN:
        import getpass
        bot_server.api_token = getpass.getpass('Enter token: ')
    bot_server.run()
