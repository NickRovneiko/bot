from django.shortcuts import render

from trader.models import Strategy, Position, Trades
from django.db.models import Sum


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
        strat.start=Position.objects.filter(strat=strat.name).order_by('opened').first().opened

        if strat.balance>strat.amount:
            active_list_strats.append(strat)
        else:
            stop_list_strats.append(strat)


    return render(request, 'trader/main.html',
                  {'list_strats':active_list_strats,
                   'stop_list_strats':stop_list_strats})