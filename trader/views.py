from django.shortcuts import render, HttpResponse, redirect

from trader.models import Variants, Position

from icecream import ic
from datetime import datetime

from .view import engine


def main(request):
    if request.GET.get('del'):
        Position.objects.filter(varian=Variants.objects.get(id=request.GET['del']).name).delete()
        return redirect('/')

    list_varian = Variants.objects.all()

    active_list_strats = []
    stop_list_strats = []

    for varian in list_varian:
        varian.open = Position.objects.filter(varian=varian.name, active=True).count()
        varian.closed = Position.objects.filter(varian=varian.name, active=False).count()
        varian.profit = round(
            sum(Position.objects.filter(varian=varian.name, active=False).values_list('profit', flat=True)), 5)
        try:
            amount_in_open = Position.objects.filter(varian=varian.name, active=True).values_list('buy_price',
                                                                                                      'amount_base')
            summa=sum([position[0] * position[1] for position in amount_in_open])
            varian.balance = round(varian.start_balance - summa + varian.profit, 4)
        except:
            pass

        if Position.objects.filter(varian=varian.name).exists():
            varian.opened = Position.objects.filter(varian=varian.name).order_by('opened').first().opened
            varian.opened = datetime.fromtimestamp(varian.opened / 1000).strftime('%Y-%m-%d %H:%M')

        if Position.objects.filter(varian=varian.name).exists():
            varian.last = Position.objects.filter(varian=varian.name).order_by('opened').last().opened
            varian.last = datetime.fromtimestamp(
                Position.objects.filter(varian=varian.name).order_by('opened').last().opened / 1000).strftime(
                '%Y-%m-%d %H:%M')

        # if varian.balance > varian.amount:
        #     active_list_strats.append(varian)
        # else:
        #     stop_list_strats.append(varian)

        active_list_strats.append(varian)
    return render(request, 'trader/main.html',
                  {'list_strats': active_list_strats,
                   'stop_list_strats': stop_list_strats})


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

def varian_view(request):
    varian=request.GET.get('varian')




