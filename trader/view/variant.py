



def Run():
    # загружаю цены
    for market in list_markets:
        if market[0] not in currentPrices:
            currentPrices[market[0]] = {}

        try:

            currentPrices[market[0]].update({market[1]: api.getMarketPrice(market[0], market[1])})
        except:
            Logs(text=f'ошибка в загрузке цен {market}').save()

    for strat in strats:

        # без котировки , переключаемся на след стратегию
        if strat.exchange in currentPrices:
            if strat.pair in currentPrices[strat.exchange]:
                price = currentPrices[strat.exchange][strat.pair]
            else:
                continue
        else:
            continue

        run_strat(strat, price)