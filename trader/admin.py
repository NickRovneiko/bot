from django.contrib import admin

from django.db import models
from django.forms import TextInput, Textarea

from .models import Trades, Variants, Position, Logs, History, Strategies, Tests, Options, Trans


class TradesAdmin(admin.ModelAdmin):
    list_display = ('varian','types', 'price', 'created')
    list_filter = ['varian','types']
    actions_on_bottom = True
    actions_on_top = True


admin.site.register(Trades, TradesAdmin)


class VariantsAdmin(admin.ModelAdmin):
    list_display = ('name','exchange','pair','start_balance','finish')
    list_editable = ['pair','start_balance']
    search_fields = ['name',]
    list_filter = ['finish','finish', 'type']
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
    list_filter = []
    actions_on_bottom = True
    actions_on_top = True


admin.site.register(Strategies, StrategiesAdmin)

class TestsAdmin(admin.ModelAdmin):
    list_display = ('name', 'win_rate','profit', 'text')
    list_filter = ['pair']
    search_fields = ['pair',]
    actions_on_bottom = True
    actions_on_top = True


admin.site.register(Tests, TestsAdmin)

class OptionsAdmin(admin.ModelAdmin):
    list_display = ['varian', 'buy_price', 'expiration' ,'strike']
    list_filter = ['active']
    search_fields = []
    actions_on_bottom = True
    actions_on_top = True


admin.site.register(Options, OptionsAdmin)

class TransAdmin(admin.ModelAdmin):
    list_display = ('varian', 'amount', 'desc', 'created')
    list_filter = ['varian','created']
    search_fields = ['desc']
    actions_on_bottom = True
    actions_on_top = True


admin.site.register(Trans, TransAdmin)
