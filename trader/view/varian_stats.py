from trader.models import  Position

from datetime import datetime

from icecream import  ic



def get_varian_stats(list_varian):
    list_varians = []

    for varian in list_varian:
        varian.open = Position.objects.filter(varian=varian.name, active=True).count()
        varian.closed = Position.objects.filter(varian=varian.name, active=False).count()
        varian.profit = round(
            sum(Position.objects.filter(varian=varian.name, active=False).values_list('profit', flat=True)), 5)
        try:
            amount_in_open = Position.objects.filter(varian=varian.name, active=True).values_list('buy_price',
                                                                                                  'amount_base')
            ic(varian.name, amount_in_open)
            summa = sum([position[0] * position[1] for position in amount_in_open])
            varian.balance = round(varian.start_balance - summa + varian.profit, 4)

            # месячная доходность в процентах
            varian.month_profit = round(varian.profit / varian.start_balance * 100 * (30 / ((Position.objects.filter(
                varian=varian.name).first().opened - Position.objects.filter(
                varian=varian.name).last().opened) / 86400000)))

            # по отношению к hold
            varian.if_hold=round((varian.profit / varian.start_balance * 100) - Position.objects.filter(
                varian=varian.name).first().buy_price/Position.objects.filter(
                varian=varian.name).last().buy_price*100-100)

            varian.win_rate=round(Position.objects.filter(varian=varian.name,profit__gte=0).count()/Position.objects.filter(varian=varian.name).count()*100)

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

        list_varians.append(varian)




    return list_varians
