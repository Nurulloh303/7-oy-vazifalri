from django.urls import path
from .views import HomeView, about, MovieCreateView, MovieDeleteView, MovieUpdateView, MovieByGenres, ByMovie, profile, MainView

urlpatterns = [
    path('', HomeView.as_view(), name='main'),
    path('about/', about, name='about'),
    path('movie/add/', MovieCreateView.as_view(), name='add_movie'),
    path('movie/<int:movie_id>/delete/', MovieDeleteView.as_view(), name='delete_movie'),
    path('movie/<int:movie_id>/update/', MovieUpdateView.as_view(), name='update_movie'),
    path('genre/<int:genre_id>/', MovieByGenres.as_view(), name='by_genre'),
    path('movie/<int:movie_id>/', ByMovie.as_view(), name='by_movie'),
    path('profile/<str:username>', profile, name='profile'),
    path("home/", MainView.as_view(), name="home"),
]
