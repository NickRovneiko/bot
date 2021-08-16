from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




class Trades(models.Model):
    strat = models.CharField(max_length=250, null=False, blank=False, verbose_name='Название')
    types = models.CharField(max_length=25, null=False, blank=False, verbose_name='Тип')
    price = models.DecimalField(max_digits=12, decimal_places=4, null='Цена')
    amount_usd =models.DecimalField(max_digits=12, decimal_places=4, null='USD')
    amount_eth = models.DecimalField(max_digits=12, decimal_places=6, null='ETH')
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
    varian = models.CharField(max_length=250, null=False, blank=False, verbose_name='Вариант')
    buy_price = models.DecimalField(max_digits=12, decimal_places=6,null=False, blank=False, verbose_name='Покупка')
    sell_price = models.DecimalField(max_digits=12, decimal_places=6,null=True, blank=True, verbose_name='Продажа')
    strike = models.DecimalField(max_digits=12, decimal_places=6,null=True, blank=True, verbose_name='Страйк')
    amount_eth = models.DecimalField(max_digits=12, decimal_places=6,null=True, blank=True, verbose_name='ETH')
    opened = models.IntegerField(null=False, verbose_name='Открыт')
    closed = models.IntegerField(null=True, verbose_name='Закрыт')
    active = models.BooleanField(default='True', verbose_name='Активен')
    profit = models.DecimalField(max_digits=12, decimal_places=6,null=True, blank=True, verbose_name='Прибыль')

    class Meta:
        ordering = ['-opened']
        verbose_name = "Позиция"
        verbose_name_plural = "Позиции"

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.buy_price)


class Variants(models.Model):
    name = models.CharField(max_length=250, unique=True, null=False, blank=False, verbose_name='Название')
    type=models.CharField(max_length=250, null=False, blank=False, verbose_name='Тип')
    exchange = models.CharField(max_length=250, null=False, blank=False, verbose_name='Биржа')
    balance_usd = models.DecimalField(max_digits=12, decimal_places=2,null=False, blank=False, verbose_name='стартовый USD')
    pair = models.CharField(max_length=25, null=False, blank=False, verbose_name='Пара')
    step = models.DecimalField(max_digits=12, decimal_places=2,null=True, blank=True, verbose_name='Шаг позиции')
    limit_orders_buy = models.BooleanField(default=False, verbose_name='Закупка по лимитам')
    amount = models.DecimalField(max_digits=12, decimal_places=2,null=True, blank=True, verbose_name='Сумма сделки')
    profit_percent = models.DecimalField(max_digits=12, decimal_places=2,null=True, blank=True, verbose_name='Процент прибыли')

    class Meta:
        ordering = ['name']
        verbose_name = "Вариант"
        verbose_name_plural = "Варианты"

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


class History(models.Model):
    exchange = models.CharField(max_length=250, null=False, blank=False, verbose_name='Биржа')
    pair = models.CharField(max_length=25, null=False, blank=False, verbose_name='Пара')
    timestamp = models.IntegerField(null=False, verbose_name='Время')
    open = models.DecimalField(max_digits=12, decimal_places=4, null=False)
    high = models.DecimalField(max_digits=12, decimal_places=4, null=False)
    low = models.DecimalField(max_digits=12, decimal_places=4, null=False)
    close = models.DecimalField(max_digits=12, decimal_places=4, null=False)
    volume = models.DecimalField(max_digits=14, decimal_places=4, null=False)

    class Meta:
        ordering = ['timestamp']
        # unique_together = ('exchange', 'pair', 'timestamp')
        verbose_name = "Котировка"
        verbose_name_plural = "Котировки"

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.exchange)


class Strategies(models.Model):
    name = models.CharField(max_length=250, unique=True, null=False, blank=False, verbose_name='Название')
    choiceStatus = (
        ('Pending', 'Неактивна'),
        ('Testing', 'Бэктест'),
        ('Online', 'Онлайн')
    )
    status = models.CharField(max_length=50, default='Pending', choices=choiceStatus, verbose_name='Статус')
    variants = models.CharField(max_length=50, verbose_name='Варианты')

    class Meta:
        ordering = ['name']
        verbose_name = "Стратегия"
        verbose_name_plural = "Стратегии"

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.name)
