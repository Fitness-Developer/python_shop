from Purchased.models import Purchased
from .models import ReviewsOfProduct
from django.forms import ModelForm
from django import forms


class PayForm(ModelForm):
    class Meta:
        model = Purchased
        fields = ['email']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'input_search', 'placeholder': 'Введите ваш email'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewsOfProduct
        fields = ['memo']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.instance.author = user