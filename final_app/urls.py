from . import views
from django.urls import path

urlpatterns = [
# path('',views.home,name='home'),
    path('', views.index, name='index'),  # Define the root URL pattern
    path('profile/', views.profile, name='profile'),
    path('movie/<int:movie_id>/', views.detail, name='detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('add/', views.add_movie, name='add_movie'),
    path('login-page/', views.login_page, name='login-page'),
    path('update/<int:movie_id>/', views.update_movie, name='update_movie'),
    path('delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('deleting-credential/<int:movie_id>/', views.deleting_credential, name='deleting_credential'),
    path('user_rating/<int:movie_id>/',views.user_rating,name='user_rating'),
    path('add_rating/<int:movie_id>/', views.add_rating, name='add_rating'),
    

    path('dashboard/movie_category/<int:category_id>/', views.movie_category, name='movie_category'),



    path('search/',views.searchResult,name='searchresult'),
    path('rating/<int:movie_id>/', views.rating, name='rating'),
    # path('add_review/<int:movie_id>/', views.add_review, name='add_review'),

]
