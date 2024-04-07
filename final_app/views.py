from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import MovieForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from .models import Movie, Rating, Review,Category
from .forms import RatingForm, ReviewForm
from django.utils import timezone
from django.db.models import Avg

# Create your views here.

def home(request):
    return render(request,'home.html')

def index(request):
    movie = Movie.objects.all()
    return render(request,'index.html',{'movie': movie})

def user_rating(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    ratings = Rating.objects.filter(movie=movie)
    avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']

    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        review_text = request.POST.get('review_text')
        user = request.user
        try:
            rating_value = float(rating_value)
            if not (0.0 <= rating_value <= 10.0):
                raise ValueError("Invalid rating value")
        except ValueError:
            messages.error(request, 'Invalid rating value. Please enter a number between 0 and 10.')
            return redirect('user_rating', movie_id=movie_id)
         # Check if the user has already rated the movie
        existing_rating = Rating.objects.filter(user=user, movie=movie).first()
        if existing_rating:
            # Update the existing rating and review
            existing_rating.rating = rating_value
            existing_rating.review = review_text
            existing_rating.save()
        else:
            # Create a new rating and review
            Rating.objects.create(user=user, movie=movie, rating=rating_value, review=review_text)
            
        messages.success(request, 'Your rating has been saved successfully.')
        return redirect('user_rating', movie_id=movie_id)

    return render(request, 'user_rating.html', {'movie': movie, 'ratings': ratings, 'avg_rating': avg_rating})


def detail(request,movie_id):
    movie = Movie.objects.get(id = movie_id)
    ratings = Rating.objects.filter(movie=movie).all()
    reviews = Review.objects.filter(movie=movie)
    rating_form = RatingForm()
    review_form = ReviewForm()
   
    avg_rating = ratings.aggregate(Avg('rating'))['rating__avg'] or 0
    context = {
        'movie': movie,
        'ratings': ratings,
        'reviews': reviews,
        'rating_form': rating_form,
        'review_form': review_form,
        "avg_rating": avg_rating
    }
    return render(request, 'detail.html', context)


# @login_required
# def add_rating(request, movie_id, rating):
#     rating = Rating.objects.all()
#     if request.method == 'POST':
#         rating = request.POST.get('rating')
#         if rating != None :
#             rating_data = Rating(movie_id=movie_id, rating=rating, user_id=request.user, created_at=timezone.now())
#             rating_data.save()
#             print("add_rating details",rating_data)
#             return redirect('/')
#         else:
#             messages.error(request, 'Please fill in all required fields.')
#             return redirect('/')
         
#     return render(request, 'detail.html', {'movie_id' : movie_id, 'rating' : rating})


# @login_required
# def add_review(request, movie_id, review_text):
#     movie = Movie.objects.get(pk=movie_id)
    
#     review = Review.objects.create(user=request.user, movie=movie, text=review_text)

#     review.save()
#     return redirect('detail', movie_id=movie_id)


from django.shortcuts import get_object_or_404
@login_required
def add_rating(request, movie_id):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_id)
    rating_value = request.POST.get('rating')
    rating_value = 0 if rating_value == '' else rating_value
    review_text = request.POST.get('review_text')
    if rating_value is not None and review_text:
        rating_value = float(rating_value)
        if 0.0 <= rating_value <= 10.0:
            # Check if the user has already rated the movie
            existing_rating = Rating.objects.filter(user=user, movie=movie).first()
            if existing_rating:
                # Update the existing rating and review
                existing_rating.rating = rating_value
                existing_rating.review = review_text
                existing_rating.save()
            else:
                # Create a new rating and review
                Rating.objects.create(user=user, movie=movie, rating=rating_value, review=review_text)
            return redirect('detail', movie_id=movie_id)
        else:
            # Handle invalid rating value
            pass
    else:
        # Handle missing rating value or review text
        pass
    # Handle invalid POST request or missing data
    # You may want to redirect the user back to the movie detail page with an error message
    return redirect('detail', movie_id=movie_id)

















        # if rating is not None and review_text is not None:
        #     rating_review_data = Rating(rating=rating, review_text=review_text, created_at=timezone.now(), movie=movie, user=request.user)
        #     rating_review_data.save()                                      
        #     print("Rating added:", rating_review_data)
        #     return redirect('detail', movie_id=movie_id)
        # else:
        #     return HttpResponse("Error: Rating value not provided")
    # return render(request, 'detail.html', {'movie': movie})



# @login_required
# def add_rating(request):
#     # movie = get_object_or_404(Movie, pk=movie_id)
#     ratings = None

#     if request.method == 'POST':
#         form = RatingForm(request.POST)
#         if form.is_valid():
#             ratings = form.save(commit=False)
#             ratings.user = request.user
#             ratings.created_at = timezone.now()
#             ratings.save()
#             messages.success(request,"The review and rating was given.")
#             print("Rating added:", ratings)
#             return redirect('index')       
#         else:
#             messages.error(request, "form not valid")
#             return redirect('register')
#     else:
#         form = RatingForm()
#         messages.info(request,"form not found")

#     return render(request, 'detail.html', {'form': form, 'ratings':ratings})




def register(request):
    if request.method == "POST":
        Ausername = request.POST.get('username', '')
        Afirst_name = request.POST['first_name']

        Alast_name = request.POST['last_name']
        Aemail = request.POST['email']
        Apassword = request.POST['password']
        Apassword1 = request.POST['password1'] 

        if not all([Ausername, Afirst_name, Alast_name, Aemail, Apassword, Apassword1]):
            messages.error(request, "Please fill all the fields! Then Register Again")
            return redirect('register')
        
        if Apassword == Apassword1:
            if User.objects.filter(username=Ausername).exists():
                messages.error(request, "Username Already Taken!! Try Another.")
                return redirect('register')
            elif User.objects.filter(email=Aemail).exists():
                messages.error(request, "Email Taken!!!")
                return redirect('register')
            else:
                user = User.objects.create_user(username=Ausername, first_name=Afirst_name, last_name=Alast_name, email=Aemail, password=Apassword)
                user.save()
                messages.success(request, "Registration Successful")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match")
            return redirect('register')
    return render(request,'register.html')


def login(request):
    if request.method == 'POST':
        username00 = request.POST['username']
        password00 = request.POST['password']

        user = auth.authenticate(username = username00, password = password00)

        if not all([username00, password00]):
            messages.info(request, "Please fill all the fields! Then Login Again")
            return redirect('login')
        
        if user is not None:
            auth.login(request,user)
            messages.success(request,"Log In Successful")
            return redirect('index')
        
        else:
            # messages.info(request,"INVALID CREDENTIALS")
            return redirect('login')

    return render(request,"login.html")

def logout(request):
    auth.logout(request)
    return redirect('index')

@login_required
def profile(request):
    movie = Movie.objects.filter(added_by=request.user)
    return render(request, 'profile.html', {'movie': movie})

def login_page(request):
    return render(request, 'login_credentials.html')

@login_required
def add_movie(request):
    movie = None  # Define movie variable
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        img = request.FILES.get('img')
        description = request.POST.get('description')
        release_date = request.POST.get('release_date')
        actors = request.POST.get('actors')
        category = request.POST.get('category')
      
        trailer_link = request.POST.get('trailer_link')

        # try:
        #     category_id = int(category_id)
        # except (ValueError, TypeError):
        #     messages.error(request, 'Invalid category ID.')
        #     return redirect('add_movie')

        if category:
            category, created = Category.objects.get_or_create(category=category)
        else:
            messages.error(request, 'Please select a category.')
            return redirect('add_movie')

        if title and description and release_date and img and actors and category and trailer_link:
            movie = Movie(title=title, description=description, release_date=release_date, img=img, actors=actors, category=category, trailer_link=trailer_link,added_by=request.user)
            movie.save()
            print("movieDetails",movie)
            messages.success(request, 'Movie Added!')
            return redirect('index')
        else:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('add_movie')
         
    return render(request, 'add_movie.html', {'movie': movie,'categories':categories})


@login_required
def update_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.user == movie.added_by:
        if request.method == 'POST':
            form = MovieForm(request.POST, request.FILES, instance=movie)
            if form.is_valid():
                form.save()
                messages.success(request,'Movie updated successfully')
                return redirect('profile')
        else:
            form = MovieForm(instance=movie)
        return render(request, 'update.html', {'form': form})
    else:
        return redirect('index')
    
    
@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.user == movie.added_by:
        movie.delete()
        return redirect('profile')
    else:
        raise Http404("You are not authorized to delete this movie.")
    
def deleting_credential(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'deleting_credential.html', {'movie': movie})
    

































from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Avg
from final_app.models import Movie,Rating
from final_app.views import detail
# Create your views here.
def searchResult(request,movie_id=None):
    movie=None
    query=None
    # movie = Movie.objects.get(id = movie_id)
    # ratings = Rating.objects.filter(movie=movie).all()
    # movie = get_object_or_404(Movie, pk=movie_id)

    if 'q' in request.GET:
        query = request.GET.get('q')
        if query.isalnum():
            
            movie = Movie.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request,'search.html',{'query':query,'movie':movie,'movie_id':movie_id})

    movie = None
    query = None

    if 'q' in request.GET:
        query = request.GET.get('q')
        if query.isalnum():
            movie = Movie.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).first()
            movie_id = None
            if movie:
                movie_id = movie.id

    return render(request, 'search.html', {'query': query, 'movie': movie, 'movie_id': movie_id})


 
 
 
 
 
 
@login_required
def rating(request, movie_id):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_id)
    rating_value = request.POST.get('rating')
    rating_value = 0 if rating_value == '' else rating_value
    review_text = request.POST.get('review_text')
    if rating_value is not None and review_text:
        rating_value = float(rating_value)
        if 0.0 <= rating_value <= 10.0:
            # Check if the user has already rated the movie
            existing_rating = Rating.objects.filter(user=user, movie=movie).first()
            if existing_rating:
                # Update the existing rating and review
                existing_rating.rating = rating_value
                existing_rating.review = review_text
                existing_rating.save()
            else:
                # Create a new rating and review
                Rating.objects.create(user=user, movie=movie, rating=rating_value, review=review_text)
            return redirect('detail', movie_id=movie_id)
        else:
            # Handle invalid rating value
            pass
    else:
        # Handle missing rating value or review text
        pass
    # Handle invalid POST request or missing data
    # You may want to redirect the user back to the movie detail page with an error message
    return redirect('detail', movie_id=movie_id)
 
 
 
 
 