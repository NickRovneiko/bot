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
    buy_price = models.FloatField(null=False, blank=False, verbose_name='Покупка')
    sell_price = models.FloatField(null=True, blank=True, verbose_name='Продажа')
    strike = models.FloatField(null=True, blank=True, verbose_name='Страйк')
    amount_base = models.FloatField(null=True, blank=True, verbose_name='Кол-во базового')
    opened = models.DateTimeField(null=False, verbose_name='Открыт')
    closed = models.DateTimeField(null=True, blank=True, verbose_name='Закрыт')
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


class Variants(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False, verbose_name='Название')
    pair = models.CharField(max_length=25, null=False, blank=False, verbose_name='Пара')
    type = models.CharField(max_length=250, null=False, blank=False, verbose_name='Тип')
    exchange = models.CharField(max_length=250, null=False, blank=False, verbose_name='Биржа')
    start_balance = models.FloatField(null=False, blank=False, verbose_name='Cтартовый')
    average_profit = models.CharField(max_length=100, null=True, blank=True, verbose_name='Средняя доходность')
    month_profit = models.IntegerField(null=True, blank=True, verbose_name='Доходность')
    sharp = models.FloatField(null=True, blank=True, verbose_name='Шарп')
    settings = models.CharField(max_length=250, null=True, blank=True, verbose_name='Настройка')
    indicators = models.CharField(max_length=250, null=True, blank=True, verbose_name='Индикаторы')
    finish = models.BooleanField(default=False, verbose_name='Выполнена')

    # range = models.FloatField(null=True, blank=True, verbose_name='Коридор %')
    # limit_orders_buy = models.BooleanField(default=False, verbose_name='Лимитные ордера')
    # deals = models.FloatField(null=True, blank=True, verbose_name='Количество ставок')
    # profit_percent = models.FloatField(null=True, blank=True,
    #                                    verbose_name='Процент прибыли')
    # stop_loss = models.CharField(max_length=250, default=None, null=True, blank=True, verbose_name='Стоп лосс')

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'type']
        verbose_name = "Вариант"
        verbose_name_plural = "Варианты"

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.name)


class Tests(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False, verbose_name='Название')
    pair = models.CharField(max_length=25, null=False, blank=False, verbose_name='Пара')
    type = models.CharField(max_length=250, null=False, blank=False, verbose_name='Тип')
    exchange = models.CharField(max_length=250, null=False, blank=False, verbose_name='Биржа')
    start_balance = models.FloatField(null=False, blank=False, verbose_name='Cтартовый')
    win_rate = models.IntegerField(null=False, blank=False, verbose_name='WIN %')
    profit = models.FloatField(null=False, blank=False, verbose_name='Прибыль')
    text = models.CharField(max_length=250, null=True, blank=True, verbose_name='Данные')
    finish = models.BooleanField(default=False, verbose_name='Выполнена')

    class Meta:
        ordering = ['name']
        verbose_name = "Тесты"
        verbose_name_plural = "Тесты"

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
    timeframe = models.CharField(max_length=25, null=False, choices=timeframe, verbose_name='Таймфрейм')
    timestamp = models.IntegerField(null=False, verbose_name='Время')
    open = models.FloatField(null=False)
    high = models.FloatField(null=False)
    low = models.FloatField(null=False)
    close = models.FloatField(null=False)
    volume = models.FloatField(null=False)

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
    indicators = models.CharField(max_length=250, null=True, verbose_name='Индикаторы')

    class Meta:
        ordering = ['name']
        verbose_name = "Стратегия"
        verbose_name_plural = "Стратегии"

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.name)


class Options(models.Model):
    varian = models.CharField(max_length=250, null=False, blank=False, verbose_name='Вариант')
    buy_price = models.FloatField(null=False, blank=False, verbose_name='Покупка')
    sell_price = models.FloatField(null=True, blank=True, verbose_name='Закрытие')
    strike = models.FloatField(null=True, blank=True, verbose_name='Страйк')
    expiration = models.DateTimeField(null=False, verbose_name='Экспирация')
    delta = models.FloatField(null=False, blank=True, verbose_name='Дельта')
    amount = models.FloatField(null=True, blank=True, verbose_name='Кол-во опциона')
    opened = models.DateTimeField(auto_now_add=True, null=False, verbose_name='Открыт')
    closed = models.DateTimeField(null=True, blank=True, verbose_name='Закрыт')
    active = models.BooleanField(default='True', verbose_name='Активен')

    class Meta:
        ordering = ['-opened']
        verbose_name = "Опцион"
        verbose_name_plural = "Опционы"

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.id)

class Trans(models.Model):
    varian = models.CharField(max_length=250, null=False, blank=False, verbose_name='Название')
    amount = models.FloatField(null=False, blank=False, verbose_name='Сумма')
    desc = models.CharField(max_length=250, null=False, blank=False, verbose_name='Описание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        ordering = ['-created']
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.varian)