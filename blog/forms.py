from django import forms
from django.forms import widgets
from .models import Comment
from .models import WorkExp
from django.utils.translation import gettext_lazy as _


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "body")
        widgets = {"body": widgets.Textarea(attrs={"rows": 4})}
        labels = {
            "body": _("Comment"),
        }
