from django.shortcuts import render, HttpResponse

from trader.models import Strategy, Position

from icecream import ic



def main(request):
    list_strats=Strategy.objects.all()

    active_list_strats=[]
    stop_list_strats=[]

    for strat in list_strats:
        strat.open=Position.objects.filter(strat=strat.name, active=True).count()
        strat.closed = Position.objects.filter(strat=strat.name, active=False).count()
        strat.profit=round(sum(Position.objects.filter(strat=strat.name, active=False).values_list('profit', flat=True)))
        strat.balance=round(strat.balance_usd - Position.objects.filter(strat=strat.name, active=True).count() * strat.amount +strat.profit)
        strat.range=round(strat.balance_usd/strat.amount*strat.step,1)
        if Position.objects.filter(strat=strat.name).exists():
            strat.opened=Position.objects.filter(strat=strat.name).order_by('opened').first().opened
            ic(strat.opened)


        if strat.balance>strat.amount:
            active_list_strats.append(strat)
        else:
            stop_list_strats.append(strat)

    return render(request, 'trader/main.html',
                  {'list_strats':active_list_strats,
                   'stop_list_strats':stop_list_strats})

def update_server(request):
    import git
    if True:
        ic()
        try:
            repo = git.Repo('/home/drann/bot')
        except:
            ic()
            repo = git.Repo('/Users/user/bot/')
        ic()
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse('Updated PythonAnywhere successfully', 200)
    else:
        ic()
        return HttpResponse('Wrong event type', 400)
