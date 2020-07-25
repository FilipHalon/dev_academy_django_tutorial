"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from rest_framework.authtoken import views

from example.views import hello_world, hello_name, hello_movie, hello_world_template, MovieListView, PostCreateView, \
    PostEditView, MovieDeleteView, MovieViewSet

router = routers.DefaultRouter()
router.register("movies", MovieViewSet, base_name="movies")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello_world/', hello_world, name="hello_world"),
    # re_path(r'hello/(?P<name>\w+)', hello_name),
    # path("hello/<str:name>", hello_name),
    re_path(r'hello/(?P<genre>\w+)', hello_movie),
    # path('movies/', hello_world_template),
    path("movie_list_by_class_view", MovieListView.as_view(), name="movie_list"),
    path("movie/add", PostCreateView.as_view()),
    path("movie/edit/<int:pk>/", PostEditView.as_view(), name='movie-edit'),
    re_path(r"movie/remove/(?P<id>\d+)", MovieDeleteView.as_view()),
    path("api-auth/", include("rest_framework.urls")),
    path("", include(router.urls)),
    path("api-token-auth/", views.obtain_auth_token),
]
