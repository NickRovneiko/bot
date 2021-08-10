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


# serve django via WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


django.setup()





def startBot():
    import time
    from trader.view import volat

    from trader.models import Variables



    while True:
        vars = Variables.objects.all()[0]
        volat.attempt(vars)
        time.sleep(20)




if __name__ == '__main__':
    startBot()

startBot()