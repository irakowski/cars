from django import forms
from cars.models import Rating, Car


class CarForm(forms.ModelForm):
    """
    Form for saving car instance
    """
    def __init__(self, *args, **kwargs):
        """
        Adding class for form fields
        """
        super(CarForm, self).__init__(*args, **kwargs)
        self.fields['make'].widget.attrs['class'] = 'form-control'
        self.fields['model'].widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = Car
        fields = '__all__'
        

class RatingForm(forms.ModelForm):
    """
    ModelForm for saving a Rating for a car
    """
    rate = forms.IntegerField(min_value=1, max_value=5, help_text='Value can\'t be greater than 5')

    def __init__(self, *args, **kwargs):
        """
        Overriding "empty label" for car select, 
        adding class for form input fields
        """
        super(RatingForm, self).__init__(*args, **kwargs)
        self.fields['car'].empty_label = '--Select a car to rate--'
        self.fields['car'].widget.attrs['class'] = 'form-control'
        self.fields['rate'].widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = Rating
        fields = '__all__'
