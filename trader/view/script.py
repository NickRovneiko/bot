import os
import django

from icecream import ic


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot.settings')
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