from django.contrib import admin

from django.db import models
from django.forms import TextInput, Textarea

from .models import Trades, Strategy, Position, Logs


class TradesAdmin(admin.ModelAdmin):
    list_display = ('strat','types', 'price', 'created')
    list_filter = ['strat','types']
    actions_on_bottom = True
    actions_on_top = True


admin.site.register(Trades, TradesAdmin)


class StrategyAdmin(admin.ModelAdmin):
    list_display = ('name','exchange','pair','balance_usd', 'step', 'amount', 'profit_percent')
    list_editable = ['pair','balance_usd', 'step', 'amount', 'profit_percent']
    search_fields = ['name']
    actions_on_bottom = True
    actions_on_top = True


admin.site.register(Strategy, StrategyAdmin)


class PositionAdmin(admin.ModelAdmin):
    list_display = ('strat','buy_price','strike','sell_price', 'opened', 'closed', 'profit', 'active')
    list_filter = ['strat','active']
    actions_on_bottom = True
    actions_on_top = True


admin.site.register(Position, PositionAdmin)

class LogsAdmin(admin.ModelAdmin):
    list_display = ('created', 'text')
    list_filter = ['created',]
    search_fields=['text']
    actions_on_bottom = True
    actions_on_top = True


admin.site.register(Logs, LogsAdmin)

