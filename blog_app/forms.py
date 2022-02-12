import django.forms as forms
from dal import autocomplete

from blog_app.models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'name', 'email']
        labels = {'text': 'Wpisz komentarz',
                  'name': 'Podpis*',
                  'email': 'Email*'
                  }


class PostShareForm(forms.Form):
    name = forms.CharField(max_length=32, label="Użytkownik")
    email_from = forms.EmailField(max_length=64, label="Email")
    email_to = forms.EmailField(max_length=64, label="Do")
    comment = forms.CharField(max_length=255, label="Komentarz", required=False, widget=forms.Textarea)


class SearchForm(forms.Form):
    query = forms.CharField()


class PostForm(autocomplete.FutureModelForm):
    class Meta:
        model = Post
        exclude = ['created', 'updated', ]
        widgets = {
            "tags": autocomplete.TaggitSelect2(
                url="tag_autocomplete"
            )
        }
