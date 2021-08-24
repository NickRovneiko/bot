from django.contrib import admin

from django.db import models
from django.forms import TextInput, Textarea

from .models import Trades, Variants, Position, Logs, History, Strategies


class TradesAdmin(admin.ModelAdmin):
    list_display = ('varian','types', 'price', 'created')
    list_filter = ['varian','types']
    actions_on_bottom = True
    actions_on_top = True


admin.site.register(Trades, TradesAdmin)


class VariantsAdmin(admin.ModelAdmin):
    list_display = ('name','exchange','pair','start_balance')
    list_editable = ['pair','start_balance']
    search_fields = ['name']
    list_filter = ['finish',]
    actions_on_bottom = True
    actions_on_top = True


admin.site.register(Variants, VariantsAdmin)


class PositionAdmin(admin.ModelAdmin):
    list_display = ('varian','buy_price','amount_base','sell_price', 'opened', 'closed', 'profit', 'active')
    list_filter = ['varian','active']
    search_fields = ['buy_price', 'sell_price', 'opened', 'closed']
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

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('timestamp','exchange', 'pair','timeframe','open', 'high', 'low')
    list_filter = ['exchange', 'pair','timeframe']
    search_fields = ['timestamp',]
    actions_on_bottom = True
    actions_on_top = True


admin.site.register(History, HistoryAdmin)


class StrategiesAdmin(admin.ModelAdmin):
    list_display = ('name', 'status','variants')
    # list_filter = []
    actions_on_bottom = True
    actions_on_top = True


admin.site.register(Strategies, StrategiesAdmin)
