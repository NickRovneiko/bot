from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from decimal import Decimal


class Trades(models.Model):
    strat = models.CharField(max_length=250, null=False, blank=False, verbose_name='Название')
    types = models.CharField(max_length=25, null=False, blank=False, verbose_name='Тип')
    price = models.FloatField(null=False, blank=False, verbose_name='Цена')
    amount_usd = models.FloatField(null=False, blank=False, verbose_name='USD')
    amount_eth = models.FloatField(null=False, blank=False, verbose_name='ETH')
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
    strat=models.CharField(max_length=250, null=False, blank=False, verbose_name='Название')
    buy_price = models.FloatField(null=False, blank=False, verbose_name='Покупка')
    sell_price = models.FloatField(null=True, blank=True, verbose_name='Продажа')
    strike = models.FloatField(null=True, blank=True, verbose_name='Страйк')
    amount_eth = models.FloatField(null=True, blank=True, verbose_name='ETH')
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


class Strategy(models.Model):
    name = models.CharField(max_length=250, unique=True, null=False, blank=False, verbose_name='Название')
    exchange = models.CharField(max_length=250, null=False, blank=False, verbose_name='Биржа')
    balance_usd = models.FloatField(null=False, blank=False, verbose_name='стартовый USD')
    pair = models.CharField(max_length=25,  null=False, blank=False, verbose_name='Пара')
    step = models.FloatField(null=True, blank=True, verbose_name='Шаг позиции')
    limit_orders_buy = models.BooleanField(default=False, verbose_name='Закупка по лимитам')
    amount = models.FloatField(null=True, blank=True, verbose_name='Сумма сделки')
    profit_percent = models.FloatField(null=True, blank=True, verbose_name='Процент прибыли')

    class Meta:
        ordering=['name']
        verbose_name = "Стратегия"
        verbose_name_plural = "Стратегии"

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.name)


class Logs(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    text = models.CharField(max_length=2500, null=False, blank=False, verbose_name='Текст')


    class Meta:
        verbose_name = "Лог"
        verbose_name_plural = "Логи"

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.created)
