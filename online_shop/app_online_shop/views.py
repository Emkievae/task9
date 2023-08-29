from django.shortcuts import render, redirect
# подключаем объект для выполнения http-запросов
from django.http import HttpResponse
from .models import OnlineShop
from .forms import AdvertisementForm
from django.urls import reverse

# Create your views here.

# функция, отображающая файл index.html
def index(request):
    # выгружаем все объекты из нашей БД
    online_shops = OnlineShop.objects.all()
    # создаем контекст шаблона
    context = {'online_shops': online_shops}
    return render(request, 'index.html', context)

# функция, отображающая файл top-sellers.html
def top_sellers(request):
    return render(request, 'top-sellers.html')

# функция для отображения формы объявления на сайте
def advertisement_post(request):
    # проверка, что обрабатывается POST-запрос
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        # проверка на валидность объекта form
        if form.is_valid():
            advertisement = OnlineShop(**form.cleaned_data)
            advertisement.user = request.user
            advertisement.save()
            url = reverse('main-page')
            return redirect(url)
    else:
        form = AdvertisementForm()
    context = {'form':form}
    return render(request, 'advertisement-post.html', context)
