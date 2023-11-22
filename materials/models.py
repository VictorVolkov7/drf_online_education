from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='course/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    price = models.PositiveIntegerField(default=100, verbose_name='цена')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='lesson/', verbose_name='превью', **NULLABLE)
    video_url = models.URLField(max_length=200, verbose_name='ссылка на видео', **NULLABLE)
    price = models.PositiveIntegerField(default=50, verbose_name='цена')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE, related_name='lesson')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payments(models.Model):
    PAYMENT_METHOD = (
        ('наличные', 'наличные'),
        ('перевод на счет', 'перевод на счет'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_date = models.DateField(auto_now_add=True, verbose_name='дата платежа')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE,
                                    related_name='payment')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок', **NULLABLE,
                                    related_name='payment')
    amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=150, choices=PAYMENT_METHOD, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.paid_course if self.paid_course else self.paid_lesson} - {self.amount}₽'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь',
                             **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE,
                               related_name='subscription')

    def __str__(self):
        return f'{self.user} подписан на {self.course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
