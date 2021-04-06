from django.test import TestCase
from django.urls import reverse

from .models import Car, Rating


def create_car(make, model):
    """
    Create a car with the given 'make' and 'model'
    """
    return Car.objects.create(make=make, model=model)

def create_rating_for_car(car, rate):
    """
    Add a rating with for the given car
    """
    return Rating.objects.create(car=car, rate=rate)


class CarModelTests(TestCase):
    
    def test_average_rating_none(self):
        """
        Avg_rating returns None for cars with no rating
        """
        car = create_car(make='Model', model='Testing')
        self.assertIsNone(car.get_avg_rating())

    def test_average_rating_value(self):
        """
        Getting Average rating for a car
        """
        c = create_car(make='Model1', model='Testing1')
        rat1 = create_rating_for_car(car=c, rate=5)
        rat2 = create_rating_for_car(car=c, rate=4)
        self.assertAlmostEqual(c.get_avg_rating(), 4.5)


class PopularViewTests(TestCase):
    
    
    def test_general_access(self):
        """
        Verifies page loads normally and returns 200 ok on access
        """
        response = self.client.get(reverse('popular'))
        self.assertEqual(response.status_code, 200)

    def test_context_data(self):
        """
        If no cars created, an appropriate message is displayed
        """
        response = self.client.get(reverse('popular'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No cars added')
        self.assertQuerysetEqual(response.context['cars'], [])
        
    def test_most_popular_cars(self):
        """
        Verifies 'popular' view lists the most rated cars in order
        """
        #3 rates for c1
        c1 = create_car(make='First', model='Car')
        r1 = create_rating_for_car(car=c1, rate=5)
        r2 = create_rating_for_car(car=c1, rate=4)
        r3 = create_rating_for_car(car=c1, rate=1)
        #4 rates for c2
        c2 = create_car(make='Second', model='Car')
        r4 = create_rating_for_car(car=c2, rate=5)
        r5 = create_rating_for_car(car=c2, rate=3)
        r6 = create_rating_for_car(car=c2, rate=5)
        r7 = create_rating_for_car(car=c2, rate=1)
        #1 rates for c3
        c3 = create_car(make='Third', model='Car')
        r6 = create_rating_for_car(car=c3, rate=5)
        
        response = self.client.get(reverse('popular'))
        self.assertQuerysetEqual(response.context['cars'], 
            ['<Car: Second Car>', '<Car: First Car>', '<Car: Third Car>'], ordered=True)


class CarCreateViewTests(TestCase):
    """
    Verifies that view displays cars form
    """
    def test_view_display(self):
        """
        Verifies page loads normally and returns 200 ok on access
        """
        response = self.client.get(reverse('create-car'))
        self.assertEqual(response.status_code, 200)

    def test_get_car_view(self):
        """
        Confirm form is in response
        """
        response = self.client.get(reverse('create-car'))
        self.assertIn('form', response.context)


    def test_success_post_car_view(self):
        """
        POST should add a car and redirect to 'popular' view
        """
        url = reverse('create-car')
        response = self.client.post(url, {'make': 'Sample', 'model': 'Car'})
        self.assertRedirects(
            response, 
            expected_url=reverse('popular'), 
            status_code=302, 
            target_status_code=200)
        self.assertTrue(Car.objects.exists())
    
    def test_car_invalid_post_data_empty_fields(self):
        """
        Invalid post data should not redirect
        Re-displays the form with validation errors
        """
        url = reverse('create-car')
        data = {
            'make': '',
            'model': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Car.objects.exists())


    def test_car_invalid_post_car_exists(self):
        """
        Uniquie constaint
        
        """
        car = create_car(make='NEW', model='CAR')
        url = reverse('create-car')
        data = {
            'make': 'NEW',
            'model': 'Car'
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Car with this Brand and Model already exists.')


class RatingViewTests(TestCase):
    
    def test_rating_view_no_cars(self):
        """
        If no car exist, an appropriate message is displayed
        """
        response = self.client.get(reverse('rate-car'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please add a car in order to give rate it')


    def test_rating_view_cars(self):
        """
        If car exist displays a form
        """
        car = create_car(make='Car', model='Test')
        response = self.client.get(reverse('rate-car'))
        self.assertIn('form', response.context)

    def test_success_post_rate_view(self):
        """
        POST should add a rating to car and redirect to 'popular' view
        """
        car = create_car(make='Car', model='For Rate')
        url = reverse('rate-car')
        response = self.client.post(url, {'car': car.id, 'rate': 5})
        self.assertRedirects(
            response, 
            expected_url=reverse('popular'), 
            status_code=302, 
            target_status_code=200)
        self.assertTrue(Rating.objects.exists())
        car.refresh_from_db()
        self.assertEqual(car.rating_set.all().count(), 1)

    
    def test_rate_invalid_rate(self):
        """
        Invalid post data should not redirect
        Re-displays the form with validation errors
        """
        car = create_car(make='CarInvalid', model='ForRate')
        url = reverse('rate-car')
        data = {'car': car.id, 'rate': 15}
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        car.refresh_from_db()
        self.assertEqual(car.rating_set.all().count(), 0)
        self.assertContains(response, 'Ensure this value is less than or equal to 5.') 