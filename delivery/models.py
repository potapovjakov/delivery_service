from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Cargo(models.Model):
    """
    Груз
    """
    pick_up = models.CharField(
        'Индекс места загрузки',
        max_length=5
    )
    delivery = models.CharField(
        'Индекс места доставки',
        max_length=5
    )
    weight = models.IntegerField(
        'Вес груза',
        validators=[
            MinValueValidator(
                1,
                message='Вес должен быть больше 0',
            ),
            MaxValueValidator(
                1000,
                message='Вес не может превышать 1000',
            )
        ]
    )
    created_at = models.DateTimeField(
        'Время создания груза',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        'Время изменения груза',
        auto_now=True
    )
    description = models.CharField(
        'Описание груза',
        max_length=500
    )

    class Meta:
        verbose_name = 'Груз'
        verbose_name_plural = 'Грузы'
        ordering = ('-created_at',)


class Truck(models.Model):
    """
    Машина
    """
    number = models.CharField(
        'Номер',
        max_length=5,
        unique=True,
    )
    location = models.CharField(
        'Индекс текущего месторасположения автомобиля',
        max_length=5,
    )
    load_capacity = models.IntegerField(
        'Грузоподъемность',
        validators=[
            MinValueValidator(
                1,
                message='Грузоподъемность должна быть больше 0',
            ),
            MaxValueValidator(
                1000,
                message='Грузоподъемность не может превышать 1000',
            )
        ]
    )

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'
