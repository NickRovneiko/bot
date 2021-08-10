from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from decimal import Decimal



class Trades(models.Model):
    types = models.CharField(max_length=25, null=False, blank=False , verbose_name='Тип')
    price = models.FloatField(null=False, blank=False, verbose_name='Цена')
    amount_usd = models.FloatField(null=False, blank=False, verbose_name='USD')
    amount_eth = models.FloatField(null=False, blank=False, verbose_name='ETH')
    balance_usd = models.FloatField(null=False, blank=False, verbose_name='Баланс USD')
    balance_eth = models.FloatField(null=False, blank=False, verbose_name='Баланс ETH')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')


    class Meta:
        ordering = ['-created']
        verbose_name = "Трейд"
        verbose_name_plural = "Трейды"

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.types)





class Position(models.Model):

    buy_price=models.FloatField(null=False, blank=False, verbose_name='Покупка')
    sell_price=models.FloatField(null=True, blank=True, verbose_name='Страйк')
    amount_eth=models.FloatField(null=True, blank=True, verbose_name='ETH')
    opened = models.DateTimeField(auto_now_add=True, verbose_name='Открыт')
    closed = models.DateTimeField(max_length=50, null=True, blank=True, verbose_name='Закрыт')
    active = models.BooleanField(default='True', verbose_name='Активен')
    profit = models.FloatField(null=True, blank=True, verbose_name='Прибыль')

    class Meta:
        ordering = ['-opened']
        verbose_name = "Позиция"
        verbose_name_plural = "Позиции"

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.buy_price)


class Variables(models.Model):

    balance_usd = models.FloatField(null=False, blank=False, verbose_name='USD')
    balance_eth = models.FloatField(null=False, blank=False, verbose_name='ETH')
    step = models.FloatField(null=True, blank=True, verbose_name='Шаг позиции USD')
    amount = models.FloatField(null=True, blank=True, verbose_name='Сумма сделки USD')
    profit_percent = models.FloatField(null=True, blank=True, verbose_name='Процент прибыли')

    class Meta:
        verbose_name = "Переменная"
        verbose_name_plural = "Переменные"

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.balance_usd)