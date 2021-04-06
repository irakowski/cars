"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cars import views as general_views

urlpatterns = [
    path('popular/', general_views.Popular.as_view(), name='popular'), 
    path('cars/', general_views.CreateCar.as_view(), name='create-car'),
    path('rate/', general_views.RateCar.as_view(), name='rate-car'),
    path('admin/', admin.site.urls),
]

handler500 = 'cars.views.my_500_view'
handler404 = 'cars.views.my_404_view'