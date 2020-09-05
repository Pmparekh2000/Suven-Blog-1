from django import forms

# Note forms can reside anywhere in the Django application but the convention is that it must be inside the forms.py file

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)