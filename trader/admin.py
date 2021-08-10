from django.contrib import admin

from django.db import models
from django.forms import TextInput, Textarea

from .models import Trades, Strategy, Position


class TradesAdmin(admin.ModelAdmin):
    list_display = ('strat','types', 'price', 'balance_usd', 'balance_eth', 'created')
    list_filter = ['strat','types']
    actions_on_bottom = True
    actions_on_top = True


admin.site.register(Trades, TradesAdmin)


class StrategyAdmin(admin.ModelAdmin):
    list_display = ('name','exchange','balance_usd', 'balance_eth', 'step', 'amount', 'profit_percent')
    list_editable = ['balance_usd','balance_eth', 'step', 'amount', 'profit_percent']
    actions_on_bottom = True
    actions_on_top = True


admin.site.register(Strategy, StrategyAdmin)


class PositionAdmin(admin.ModelAdmin):
    list_display = ('strat','buy_price', 'sell_price', 'opened', 'closed', 'profit', 'active')
    list_filter = ['strat','active']
    actions_on_bottom = True
    actions_on_top = True


admin.site.register(Position, PositionAdmin)
from django.contrib import admin

# Register your models here.
