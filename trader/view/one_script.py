import os
import django

import sys

try:
    project_home = '/home/drann/bot'
    if project_home not in sys.path:
        sys.path.insert(0, project_home)
except:
    project_home='/Users/user/bot/'
    if project_home not in sys.path:
        sys.path.insert(0, project_home)

os.environ['DJANGO_SETTINGS_MODULE'] = 'bot.settings'

django.setup()


def startBot():
    from trader.view import engine

    from trader.models import Variants

    engine.attempt()




if __name__ == '__main__':
    startBot()