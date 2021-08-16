from django.shortcuts import render, HttpResponse

from trader.models import Variants, Position

from icecream import ic
from datetime import datetime

from .view import engine





def main(request):
    ask_delete=False
    if request.GET.get('del'):
        ic()
        if request.GET.get('ask_delete'):
            ic()
            engine.delete_varian(request)
        else:
            ic()
            ask_delete=request.GET.get('del')


    list_varian=Variants.objects.all()

    active_list_strats=[]
    stop_list_strats=[]

    for varian in list_varian:
        varian.open=Position.objects.filter(varian=varian.name, active=True).count()
        varian.closed = Position.objects.filter(varian=varian.name, active=False).count()
        varian.profit=round(sum(Position.objects.filter(varian=varian.name, active=False).values_list('profit', flat=True)))
        varian.balance=round(varian.balance_usd - Position.objects.filter(varian=varian.name, active=True).count() * varian.amount +varian.profit)
        varian.range=round(varian.balance_usd/varian.amount*varian.step,1)
        if Position.objects.filter(varian=varian.name).exists():
            varian.opened=Position.objects.filter(varian=varian.name).order_by('opened').first().opened
            varian.opened= datetime.fromtimestamp(varian.opened/1000).strftime('%Y-%m-%d %H:%M')



        if varian.balance>varian.amount:
            active_list_strats.append(varian)
        else:
            stop_list_strats.append(varian)

    return render(request, 'trader/main.html',
                  {'list_strats':active_list_strats,
                   'stop_list_strats':stop_list_strats,
                   'ask_delete':ask_delete})

def update_server(request):
    import git
    if True:
        try:
            repo = git.Repo('/home/drann/bot')
        except:
            repo = git.Repo('/Users/user/bot/')
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse('Updated PythonAnywhere successfully', 200)
    else:
        return HttpResponse('Wrong event type', 400)
