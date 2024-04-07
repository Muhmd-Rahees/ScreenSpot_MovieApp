from django.db.models import Avg
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=50)
    img = models.ImageField(upload_to='gallery', null=True, blank=True)
    description = models.TextField(max_length=800)
    release_date = models.DateField()
    actors = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    trailer_link = models.URLField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def average_rating(self):
        return self.rating_set.aggregate(Avg('rating'))['rating__avg']

    def __str__(self):
        return self.title

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField()
    review = models.TextField(max_length=500,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    