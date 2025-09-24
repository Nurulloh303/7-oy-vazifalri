from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib import messages
from .models import Genre, Movie, Profile
from .forms import MovieForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View
from django.urls import reverse_lazy




class HomeView(ListView):
    template_name = 'moviesite/main.html'
    context_object_name = 'movies'
    extra_context = {
        'title': 'Home',
        'genres': Genre.objects.all(),
    }

    def get_queryset(self):
        return Movie.objects.filter(published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        return context




def about(request: HttpRequest):
    context = {
        'title': 'about',
    }

    return render(request, 'moviesite/about.html', context)

class MovieByGenres(HomeView):
    def get_queryset(self):
        queryset = Movie.objects.filter(published=True, genre_id=self.kwargs['genre_id'])
        return queryset




# #
# def by_movie(request: HttpRequest, movie_id):
#     movie = get_object_or_404(Movie, pk=movie_id, published=True)
#
#     movie.views += 1
#     movie.save()
#
#     context = {----
#         'movie': movie,
#         'title': movie.title,
#     }
#
#     return render(request, 'moviesite/movie.html', context)

# POST
# ==========================
# Movie CRUD (Class-based Views)
# ==========================
class MovieCreateView(CreateView):
    model = Movie
    form_class = MovieForm
    template_name = "moviesite/add_movie.html"
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        messages.success(self.request, "Maqola muvaffaqiyatli qo'shildi!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ma'lumotlar qo'shishda xatolik yuz berdi!")
        return super().form_invalid(form)


class MovieUpdateView(UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = "moviesite/update_movie.html"  # update_movie funksiyasidagi template
    pk_url_kwarg = "movie_id"
    success_url = reverse_lazy("main")

    def form_valid(self, form):
        messages.success(self.request, "Film muvaffaqiyatli yangilandi!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ma'lumotlarni yangilashda xatolik yuz berdi!")
        return super().form_invalid(form)


class MovieDeleteView(DeleteView):
    model = Movie
    template_name = "moviesite/delete_movie.html"  # delete_movie funksiyasidagi template
    pk_url_kwarg = "movie_id"
    success_url = reverse_lazy("main")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Film muvaffaqiyatli o'chirildi!")
        return super().delete(request, *args, **kwargs)


login_required(login_url='/login/')
def profile(request: HttpRequest, username: str):
    profile_user = get_object_or_404(User, username=username)

    context = {
        'profile_user': profile_user,
        'title': str(profile_user.username).title() + "profil"
    }

    try:
        profile = Profile.objects.get(user=profile_user)
        context["profile"] = profile
    except:
        pass

    return render(request, 'profile.html', context)

class MainView(View):
    def get(self, request):
        context = {
            "title": "Asosiy sahifa",
            "welcome": "Hush kelibsiz",
        }
        return render(request, 'moviesite/main.html', context)


# def movie_detail(request: HttpRequest, movie_id: int):
#     genres  = Genre.objects.all()
#     movie = get_object_or_404(Movie, pk=movie_id)
#
#     context = {
#         'genres': genres,
#         'movie': movie,
#         'title': str(movie.title).title(),
#     }
#
#     return render(request, 'moviesite/movie_detail.html', context)

class ByMovie(DetailView):
    model = Movie
    pk_url_kwarg = 'movie_id'
    template_name = "moviesite/movie.html"
    context_object_name = "movie"   # << muhim

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()
        movie.views += 1
        movie.save()
        context['title'] = movie.title
        context['genres'] = Genre.objects.all()
        return context
