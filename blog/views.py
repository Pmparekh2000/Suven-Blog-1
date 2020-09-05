from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

# Create your views here.

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    # default variable is object_list if we don't specify the above line
    paginate_by = 1
    template_name = 'blog/post/list.html'

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 1) # 3 posts on each page
    page = request.GET.get('page')
    # The above line gives the current page number
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range then deliver last page of results
        posts = paginator.page(paginator.num_pages)        
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # The save method creates an instance of the model that the form is linked to and saves to db
            # Create Comment object but don't save to db yet
            # Note the "save()" method is available to ModelForm but not for Form instances, since they are not linked to any model
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the db
            new_comment.save()
    else:
        comment_form = CommentForm()    
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})

def post_share(request, post_id):
    # Retrive post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    # By the following branching, we use the same view to show the form and processing the submitted data
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form field passed validation
            cd = form.cleaned_data
            # cleaned_data is a dictionary of the form fields which are valid, invalid fields are not included
            # ... logic for sending email is below
            post_url = request.build_absolute_uri(post.get_absolute_url())
            # We use request.build_absolute_uri() to build an absolute path url in the email to redirect it to the post
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            # Above method is used to send the email
            sent = True 
    else:
        # Form was not submitted and we need to display the empty form
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})    
    # The return statement will show the form either filled or empty depending on the validation.