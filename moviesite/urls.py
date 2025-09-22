from django.urls import path
from .views import HomeView, about, add_movie, delete_movie, update_movie, MovieByGenres, ByMovie, profile, MainView

urlpatterns = [
    path('', HomeView.as_view(), name='main'),
    path('about/', about, name='about'),
    path('movie/add/', add_movie, name='add_movie'),
    path('movie/<int:movie_id>/delete/', delete_movie, name='delete_movie'),
    path('movie/<int:movie_id>/update/', update_movie, name='update_movie'),
    path('genre/<int:genre_id>/', MovieByGenres.as_view(), name='by_genre'),
    path('movie/<int:movie_id>/', ByMovie.as_view(), name='by_movie'),
    path('profile/<str:username>', profile, name='profile'),
    path("main/", MainView.as_view(), name="main"),
]
