import django.forms as forms

from blog_app.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'name', 'email']
        labels = {'text': 'Wpisz komentarz',
                  'name': 'Podpis*',
                  'email': 'Email*'
                  }
