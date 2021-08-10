from django.contrib import admin

from django.db import models
from django.forms import TextInput, Textarea

from .models import Trades, Variables, Position


class TradesAdmin(admin.ModelAdmin):
    list_display = ('types', 'price', 'balance_usd', 'balance_eth', 'created')
    list_filter = ['types', ]
    actions_on_bottom = True
    actions_on_top = True


admin.site.register(Trades, TradesAdmin)


class VariablesAdmin(admin.ModelAdmin):
    list_display = ('balance_usd', 'balance_eth', 'step', 'amount', 'profit_percent')
    actions_on_bottom = True
    actions_on_top = True


admin.site.register(Variables, VariablesAdmin)


class PositionAdmin(admin.ModelAdmin):
    list_display = ('buy_price', 'sell_price', 'opened', 'closed', 'profit', 'active')
    list_filter = ['active']
    actions_on_bottom = True
    actions_on_top = True


admin.site.register(Position, PositionAdmin)
from django.contrib import admin

# Register your models here.
