from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets, status, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from example.forms import MovieForm
from example.models import Genre, Movie
from example.serializers import MovieSerializer, MovieMiniSerializer


# Create your views here.


def hello_world(request):
    return HttpResponse('Hello world!')


def hello_name(request, name):
    return HttpResponse(f"Hello {name}!")


def hello_movie(request, genre):
    genre = get_object_or_404(Genre, name=genre)
    movie = get_object_or_404(Movie, genre=genre)
    return render(request, 'hello.html', {'movie': movie})


def hello_world_template(request):
    movies = Movie.objects.all()
    return render(request, "index.html", {'movies': movies})


class MovieListView(ListView):
    model = Movie
    template_name = 'list.html'
    context_object_name = "movies"


class PostCreateView(CreateView):
    model = Movie
    form_class = MovieForm
    success_url = "/movie/add"
    template_name = "add.html"


class PostEditView(UpdateView):
    model = Movie
    form_class = MovieForm
    template_name = "add.html"

    @property
    def success_url(self):
        return reverse("movie_list")


class MovieDeleteView(DeleteView):
    model = Movie
    form_class = MovieForm
    template_name = "remove.html"

    @property
    def success_url(self):
        return reverse_lazy("movie_list")


class MovieViewSet(viewsets.ModelViewSet):
    # queryset dla serializatora można zdefiniować albo jako atrybut, albo funkcję get_queryset
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ("name", "year", "viewed")
    search_fields = ("name", )
    ordering_fields = ("year", "id")
    authentication_classes = (TokenAuthentication, )

    # def get_queryset(self):
    #     queryset = Movie.objects.filter(genre__name="Horror")
    #     return queryset

    def get_queryset(self):
        # dostęp do paramatrów zapytania
        # query_params = self.request.query_params
        queryset = self.queryset
        # year = query_params.get("year")
        # viewed = query_params.get("viewed")
        # sprawdza, czy to napis, czy ma 128 znaków itd.

        # if year:
        #     queryset = queryset.filter(year=year)
        #
        # if viewed:
        #     queryset = queryset.filter(viewed=viewed)

        return queryset

    # def list(self, request, *args, **kwargs):
    #     # queryset odwołuje się do właściwości klasy, a jeśli chcielibyśmy odwołać się do funkcji, to trzeba by było dać self.get_queryset()
    #     serializer = MovieMiniSerializer(self.get_queryset(), many=True)
    #     return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MovieSerializer(instance)
        return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     # na serializatorze trzeba użyć is.valid()
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def create(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def viewed(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.viewed = True
        instance.save()
        serializer = MovieSerializer(instance)
        return Response(serializer.data)

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
