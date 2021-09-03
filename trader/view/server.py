def run():
    import os, django, sys

    project_home = '/home/drann/bot'
    if project_home not in sys.path:
        sys.path.insert(0, project_home)

    os.environ['DJANGO_SETTINGS_MODULE'] = 'bot.settings'
    django.setup()