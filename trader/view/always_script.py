import os
import django

import sys

# add your project directory to the sys.path
project_home = '/home/drann/bot'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# set environment variable to tell django where your settings.py is
os.environ['DJANGO_SETTINGS_MODULE'] = 'bot.settings'

django.setup()





def startBot():
    from trader.view import engine

    while True:
        engine.online_bot()


if __name__ == '__main__':
    startBot()

startBot()