from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Location(models.Model):
    """
    Локация
    """
    city = models.CharField(
        verbose_name='Город',
        max_length=250
    )
    state_name = models.CharField(
        verbose_name='Штат',
        max_length=250
    )
    zip_code = models.CharField(
        verbose_name='Почтовый индекс',
        primary_key=True,
        db_index=True,
        max_length=5,
    )
    lng = models.CharField(
        verbose_name='Долгота',
        max_length=10
    )
    lat = models.CharField(
        verbose_name='Широта',
        max_length=10
    )

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.zip_code


class Cargo(models.Model):
    """
    Груз
    """
    pick_up = models.ForeignKey(
        Location,
        related_name='pick_up',
        verbose_name='Индекс места загрузки',
        max_length=5,
        on_delete=models.CASCADE,
    )
    delivery = models.ForeignKey(
        Location,
        related_name='delivery',
        verbose_name='Индекс места доставки',
        max_length=5,
        on_delete=models.CASCADE,
    )
    weight = models.IntegerField(
        verbose_name='Вес груза',
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
        verbose_name='Время создания груза',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Время изменения груза',
        auto_now=True
    )
    description = models.CharField(
        verbose_name='Описание груза',
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
    truck_number = models.CharField(
        verbose_name='Номер машины',
        max_length=5,
        unique=True,
    )
    current_location = models.ForeignKey(
        Location,
        verbose_name='Индекс текущего месторасположения автомобиля',
        max_length=5,
        on_delete=models.CASCADE,
    )
    load_capacity = models.IntegerField(
        verbose_name='Грузоподъемность',
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
