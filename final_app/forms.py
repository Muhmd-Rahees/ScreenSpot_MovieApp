# forms.py
from django import forms
from .models import Movie
from .models import Rating,Review
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'img', 'release_date', 'actors', 'category', 'trailer_link']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating','review','user','movie']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text']
