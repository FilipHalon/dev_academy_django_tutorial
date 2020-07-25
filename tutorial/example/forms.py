from django import forms
from example.models import Movie, Genre


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        exclude = ("created_on", )

    def clean_name(self):
        name = self.cleaned_data["name"]
        if "curse" in name.lower():
            raise forms.ValidateError("You cannot use forbidden words")
        return name


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'
