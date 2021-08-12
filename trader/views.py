from django.shortcuts import render

from trader.models import Strategy, Position, Trades



def main(request):
    list_strats=Strategy.objects.all()

    for strat in list_strats:
        strat.open=Position.objects.filter(strat=strat.name, active=True).count()
        strat.closed = Position.objects.filter(strat=strat.name, active=False).count()
        strat.profit=round(sum(Position.objects.filter(strat=strat.name, active=False).values_list('profit', flat=True)))
        strat.balance_usd=round(strat.balance_usd)
        strat.check=10000 - strat.open * strat.amount
    list_strats.order_by('-profit')


    return render(request, 'trader/main.html',
                  {'list_strats':list_strats})