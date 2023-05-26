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

