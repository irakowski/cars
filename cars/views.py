from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from . import models
from . import forms


class Popular(generic.TemplateView):
    """
    Queries five most rated cars for display in the table
    sorted by number of rates
    """
    template_name = 'cars/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = models.Car.objects.annotate(
            car_rating=Count('rating')).order_by('-car_rating')[:5]
        return context


class CreateCar(SuccessMessageMixin, generic.CreateView):
    """
    GET / cars : Displays empty CarForm for creating a car record 
    POST /rate : Saves car instance in the db table
    FormData: csrfmiddlewaretoken: value / make: value / model: value
    """
    model = models.Car
    form_class = forms.CarForm
    template_name = 'cars/car_form.html'
    success_url = reverse_lazy('popular')
    success_message = 'Car has been added'


class RateCar(SuccessMessageMixin, generic.CreateView):
    """
    GET /rate : Displays empty RatingForm. 
    POST /rate : saves rating for a specific car
    FormData: csrfmiddlewaretoken: value / car: id / rate: value 
    Redirects to 'popular' upon success, displays empty form with errors otherwise
    """
    model = models.Rating
    template_name = 'cars/rate_form.html'
    form_class = forms.RatingForm
    success_url = reverse_lazy('popular')
    success_message = 'Rating has been saved'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = models.Car.objects.all()
        return context


def my_500_view(request):
    """
    Custom 500 View
    """
    context = {}
    response = render(request, "cars/500.html", context=context)
    response.status_code = 500
    return response

def my_404_view(request, exception):
    """
    Custom 404 View 
    """
    context = {}
    response = render(request, "cars/404.html", context=context)
    response.status_code = 404
    return response


