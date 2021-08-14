import os
import django

from icecream import ic

import sys

# add your project directory to the sys.path
project_home = '/home/drann/bot'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# set environment variable to tell django where your settings.py is
os.environ['DJANGO_SETTINGS_MODULE'] = 'bot.settings'

django.setup()





def startBot():
    import time
    from trader.view import volat

    from trader.models import Strategy



    while True:
        strats = Strategy.objects.all()
        volat.attempt(strats)




if __name__ == '__main__':
    startBot()

startBot()