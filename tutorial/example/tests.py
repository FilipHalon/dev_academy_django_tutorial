from django.test import TestCase
from django.urls import reverse

from example.models import Movie, Genre
from example.forms import MovieForm


# Create your tests here.

class SimpleTestCase(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Horror")
        self.movie = Movie.objects.create(
            name="Dracula",
            year=1987,
            released="02-11-1987",
            genre=self.genre
        )
        # hello_world_url = reverse('hello_world')
        # form_view_url = reverse('name_form_view_url')

    def tearDown(self):
        self.movie.delete()
        self.genre.delete()

    def test_max_length(self):
        form = MovieForm(data={'name': 'x' * 200})
        self.assertFalse(form.is_valid())

    def test_initial(self):
        form = MovieForm(instance=self.movie)
        self.assertEqual(form.initial['name'], self.movie.name)

    def test_display_view(self):
        response = self.client.get(reverse('hello_world'))
        content = str(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.resolver_match.view_name, 'hello')

    # def test_display_view(self):
    #     data = {'name': ''}
    #     expected_error = 'expected_error_msg'
    #     response = self.client.post(self.form_view_url, data)
    #
    #     self.assertFormError(response, 'form', field_name, expected_error)
