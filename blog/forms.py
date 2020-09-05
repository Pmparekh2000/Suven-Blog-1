from django import forms
from .models import Comment

# Note forms can reside anywhere in the Django application but the convention is that it must be inside the forms.py file

# The below form is a static form (Form)
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

# The below form is a dynamic form (ModelForm)
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        # The above fields attribute is used to filter the number of fields to be made in the form

