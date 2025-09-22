from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib import messages
from .models import Genre, Movie, Profile
from .forms import MovieForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View




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
@permission_required('moviesite.add_movie', raise_exception=True)
def add_movie(request: HttpRequest):
    if request.user.is_staff:
        if request.method == 'POST':
            form = MovieForm(request.POST, files=request.FILES)
            if form.is_valid():
                movie = form.save()
                messages.success(request, "Maqola muvaffaqiyatli qo'shildi!")
                return redirect("by_movie", movie_id=movie.pk)
            else:
                messages.error(request, "Ma'lumotlar qo'shishda xatolik yuz berdi!")
        else:
            form = MovieForm()

        context = {
            "form": form,
            "title": "Film qo'shish"
        }
        return render(request, 'moviesite/add_movie.html', context)
    else:
        messages.error(request, "Sizda ruxsat yo‘q!")
        return render(request, '404.html')
    
# UPDATE
@permission_required("moviesite.change_moviesite")
def update_movie(request: HttpRequest, movie_id: int):
    if request.user.is_staff:
        movie = get_object_or_404(Movie, pk=movie_id)

        if request.method == 'POST':
            form = MovieForm(request.POST, files=request.FILES, instance=movie)
            if form.is_valid():
                movie = form.save()
                messages.success(request, "Film muvaffaqiyatli yangilandi!")
                return redirect("by_movie", movie_id=movie.pk)
            else:
                messages.error(request, "Ma'lumotlar qo'shishda xatolik yuz berdi!.")
        else:
            form = MovieForm(instance=movie)

        context = {
            "form": form,
            "title": "Filmni yangilash"
        }
        return render(request, 'moviesite/update_movie.html', context)
    else:
        messages.error(request, "Sizda ruxsat yo‘q!")
        return render(request, '404.html')
    
# DELETE
@permission_required("moviesite.delete_moviesite")
def delete_movie(request: HttpRequest, movie_id):
    if request.user.is_staff:
        movie = get_object_or_404(Movie, pk=movie_id)
        messages.warning(request, "Filmni o'chirmoqchimisiz?")
        if request.method == 'POST':
            movie.delete()
            messages.success(request, "Film muvaffaqiyatli o'chirildi!")
            return redirect("main")
        context = {
            'movie': movie,
            'title': "Filmni o'chirish"
        }
        return render(request, 'moviesite/delete_movie.html', context)
    else:
        messages.error(request, "Sizda ruxsat yo‘q!")
        return render(request, '404.html')


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
