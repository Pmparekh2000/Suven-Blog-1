from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Note User model is the default model in the Django auth

# Create your models here.

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    # CharField translates to a VARCHAR column in the SQL db
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    # slug field is the field intended to be used only in the URL as it contains only letter, numbers and underscores or hyphens
    # We can use slug field to build beautiful SEO friendly URLs.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    # author is a foreign key which defines many to one relationship
    # on_delete is used to delete the posts once the user is deleted.
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    # STATUS_CHOICES is used here so that "status" field can be set only to the two values avaiable in it

    class Meta:
        ordering = ('-publish',)
        # this class provides meta information i.e. to sort the posts on the basis of publish field in the descinding order
        # So that the most recent posts appear at the top.
    
    def __str__(self):
        return self.title