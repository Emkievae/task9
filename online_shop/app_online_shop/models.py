from django.db import models
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

# создаем класс с описание структуры будущей таблицы (наследуемся от класса Model)
class OnlineShop(models.Model):
    # создаем заголовок объявления
    # CharField - класс, обозначающий символьное поле (набор символов), подходит для небольших текстов
    title = models.CharField('Заголовок', max_length=128)
    # создаем описание объявления
    # TextField - класс, обозначающий строковое поле больших размеров
    description = models.TextField('Описание')
    # создаем цену
    # Decimal - дробное число с фиксированной точностью (похоже на float в Python)
    # max_digits - максимальное кол-во цифр в числе
    # decival_places - кол-во знаком после запятой
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    # создаем возможность торгроваться
    # BooleanField - логический тип данных (истина или ложь)
    auction = models.BooleanField('Торг', help_text='Отметьте, уместен ли торг')
    # создаем дату размещения объявления
    # auto_now_add=True - сразу получаем дату в момент создания объявления
    created_time = models.DateTimeField(auto_now_add=True)
    # создаем дату обновления объявления
    # auto_now=True - получаем дату в момент обновления объявления
    update_time = models.DateTimeField(auto_now=True)
    # поле для создателя объявления (пользователя)
    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE)
    # поле для изображения
    image = models.ImageField('Изображение', upload_to='online_shop/')

    @admin.display(description='дата создания')
    def created_date(self):
        from django.utils import timezone
        if self.created_time.date() == timezone.now().date():
            created_date = self.created_time.time().strftime("%H:%M:%S")
            return format_html(
                '<span style="color: green; font-weight: bold;">Сегодня в {}</span>', created_date
            )
        return self.created_time.strftime("%d.%m.%Y в %H:%M:%S")

    @admin.display(description='дата последнего обновления')
    def updated_date(self):
        from django.utils import timezone
        if self.update_time.date() == timezone.now().date():
            created_time = self.update_time.time().strftime("%H:%M:%S")
            return format_html(
                '<span style="color: green; font-weight: bold;">Сегодня в {}</span>', created_time
            )
        return self.update_time.strftime("%d.%m.%Y в %H:%M:%S")
    
    @admin.display(description='изображение')
    def mini_image(self):
        if self.image:
            img = self.image.url
            return format_html('<img src={}', img)
        else:
            return format_html('<img src={}', '.static/img/shop.png')
    def __str__(self):
        return f"Advertisement(id={self.id}, title={self.title}, price={self.price})"

    class Meta:
        db_table = "advertisements"

