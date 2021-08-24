from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Trades(models.Model):
    varian = models.CharField(max_length=250, null=False, blank=False, verbose_name='Название')
    types = models.CharField(max_length=25, null=False, blank=False, verbose_name='Тип')
    price = models.FloatField(verbose_name='Цена')
    base = models.FloatField(verbose_name='Базовая')
    quote = models.FloatField(verbose_name='Котировка')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        ordering = ['-created']
        verbose_name = "Трейд"
        verbose_name_plural = "Трейды"

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.varian)


class Position(models.Model):
    varian = models.CharField(max_length=250, null=False, blank=False, verbose_name='Вариант')
    buy_price = models.FloatField( null=False, blank=False, verbose_name='Покупка')
    sell_price = models.FloatField( null=True, blank=True, verbose_name='Продажа')
    strike = models.FloatField( null=True, blank=True, verbose_name='Страйк')
    amount_base = models.FloatField( null=True, blank=True, verbose_name='Кол-во базового')
    opened = models.IntegerField(null=False, verbose_name='Открыт')
    closed = models.IntegerField(null=True, verbose_name='Закрыт')
    active = models.BooleanField(default='True', verbose_name='Активен')
    profit = models.FloatField( null=True, blank=True, verbose_name='Прибыль')

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
    pair = models.CharField(max_length=25, null=False, blank=False, verbose_name='Пара')
    type = models.CharField(max_length=250, null=False, blank=False, verbose_name='Тип')
    exchange = models.CharField(max_length=250, null=False, blank=False, verbose_name='Биржа')
    start_balance = models.FloatField( null=False, blank=False, verbose_name='Cтартовый')
    settings = models.CharField(max_length=250, null=True, verbose_name='Настройка')
    indicators = models.CharField(max_length=250, null=True, verbose_name='Индикаторы')
    finish=models.BooleanField(default=False, verbose_name='Выполнена')

    # range = models.FloatField(null=True, blank=True, verbose_name='Коридор %')
    # limit_orders_buy = models.BooleanField(default=False, verbose_name='Лимитные ордера')
    # deals = models.FloatField(null=True, blank=True, verbose_name='Количество ставок')
    # profit_percent = models.FloatField(null=True, blank=True,
    #                                    verbose_name='Процент прибыли')
    # stop_loss = models.CharField(max_length=250, default=None, null=True, blank=True, verbose_name='Стоп лосс')


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
    timeframe = (
        ('1m', 'Минута'),
        ('1h', 'Час'),
    )
    timeframe = models.CharField(max_length=25,null=False, choices=timeframe, verbose_name='Таймфрейм')
    timestamp = models.IntegerField(null=False, verbose_name='Время')
    open = models.FloatField( null=False)
    high = models.FloatField( null=False)
    low = models.FloatField( null=False)
    close = models.FloatField( null=False)
    volume = models.FloatField( null=False)

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
    indicators=models.CharField(max_length=250, null=True, verbose_name='Индикаторы')

    class Meta:
        ordering = ['name']
        verbose_name = "Стратегия"
        verbose_name_plural = "Стратегии"

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.name)
