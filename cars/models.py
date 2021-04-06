from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg

class Car(models.Model):
    make = models.CharField(verbose_name=_('Brand'), max_length=128)
    model = models.CharField(max_length=128)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['make', 'model'], name='unique_car')
        ]

    def __str__(self):
        return f'{self.make} {self.model}' 

    def clean(self):
        self.make = self.make.upper()
        self.model = self.model.upper()

    def get_avg_rating(self):
        rating = Rating.objects.filter(car=self).aggregate(rating_avg=Avg('rate'))
        return (rating['rating_avg'])



class Rating(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f'{self.rate}' 
