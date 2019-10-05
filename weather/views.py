from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=8300ad68d40fe6c2288296dcf933e297'
    # url1='http://ipinfo.io'
    err_msg = ''
    message = ''
    message_class = ''
    # r1 = requests.get(url1).json()
    # print(r1)

    if request.method == 'POST':
        print(request.POST)
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg='Hey please check the city name you entered :)'
            else:
                err_msg='city already exist!!'

        if err_msg:
            message = err_msg
            message_class = 'alert alert-danger'
        else:
            message = 'City added successfully'
            message_class = 'alert alert-success'


    form = CityForm()
    weather_data = []
    cities=City.objects.values_list('name', flat=True).distinct()
    print(cities)
    for city in cities:
        r = requests.get(url.format(city)).json()
        print(r)
        # print(city+'--')
        city_weather = {
            'city' : city,
            'tempreture' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon']
        }
        weather_data.append(city_weather)
 
   # print(weather_data)
    context = {
     'weather_data':weather_data,
     'form':form,
     'message':message,
     'message_class':message_class
     }
    return render(request,'weather/index.html',context)


def delete_city(request, city_name):
    #print(city_name)
    City.objects.get(name=city_name).delete()

    return redirect('home')