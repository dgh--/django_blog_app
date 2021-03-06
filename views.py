import sys
import re

from django.shortcuts import render
from django.shortcuts import reverse

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Post
from .models import Comment

from .forms import PostForm
from .forms import CommentForm
from .forms import UserForm

from .utilities import remove_html


"""
I notice that you're using function based views rather than class based views.
This is fine; in many respects it's a question of personal preference.
But it's probably worth learning how to do this with class based views as well;
they tend to be the default approach for achieving things like this for many
Django developers these days.

CBVs can become unwieldy, though, if you're trying to get them to do things that
deviate significantly from what they were originally designed to do; if you just
want to have a page with a list of posts, then a ListView with most of the default
settings will probably serve you well. Once you find yourself in a position where
you want to do something a bit more involved than this they can become quite tricky
to work with. (IMHO the Django documentation on the subject could be better;
a useful resource to look at is http://ccbv.co.uk/ - it's a good thing to study
this to give you an idea of which methods you can override. Still. Can take a while
to get your head around it. If you prefer this approach, it's fine.) :)
"""



def index_view(request):
    """Handle requests to blog:index."""
    post_list = Post.objects.all().order_by('-posted')

    paginator = Paginator(post_list, 5)
    page = request.GET.get('page', 1)

    # If the following looks like it was lifted straight from
    # the Django documentation, that's because it was, basically:
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if not user is None:
            login(request, user)
            user_form = UserForm()
        else:
            user_form = UserForm()
            user_form.need_valid_user = True
    else:
        user_form = UserForm()  

    return render(
        request,
        'blog_app/index.html',
        {
            'posts': posts,
            'user_form': user_form
        }
    )


def post_data_view(request, pk):
    """Handle requests to blog:post_data."""
    post = Post.objects.get(pk = pk)

    comment_list = post.comments.all().order_by('-created')
    paginator = Paginator(comment_list, 5)
    page = request.GET.get('page', 1)

    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(1)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            author = remove_html(form.cleaned_data['author'])
            text = remove_html(form.cleaned_data['text'])

            text = text.replace('\n', '<br/>')            

            new_comment = Comment(
                author = author,
                text = text,
                post = post
            )
            new_comment.save()
            
            return HttpResponseRedirect(reverse('blog:post_data', args = (pk, )))
    
    else:
        form = CommentForm()
    
    return render(
        request,
        'blog_app/post_data.html',
        {
            'post': post,
            'comments': comments,
            'form': form        
        }
    )

@login_required
def create_post_view(request):
    """Handle requests to blog:create_post"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            title = remove_html(form.cleaned_data['title'])
            body = remove_html(form.cleaned_data['body'])

            body = body.replace('\n', '<br/>')

            new_post = Post(
                title = title,
                body = body
            )   
            new_post.save()

            return HttpResponseRedirect(reverse('blog:index'))
    else:
        form = PostForm()

    return render(
        request,
        'blog_app/create_post.html',
        {
            'form': form
        }
    )


@login_required
def delete_post_view(request, pk):
    """Handle requests to blog:delete_post."""
    Post.objects.get(pk = pk).delete()
    return HttpResponseRedirect(reverse('blog:index'))


def create_comment_view(request, pk):
    """Handle requests to blog:create_comment."""
    if request.POST['author'] == '' or request.POST['text'] == '':
        return HttpResponseRedirect(
            reverse('blog:post_data', args = (pk, ))
        )

    Post.objects.get(pk = pk).comments.create(
        author = request.POST['author'],
        text = request.POST['text']
    )
    return HttpResponseRedirect(reverse('blog:post_data', args = (pk, )))


@login_required
def delete_comment_view(request, post_pk, comment_pk):
    """Handle requests to blog:delete_comment."""
    Comment.objects.get(pk = comment_pk).delete()
    return HttpResponseRedirect(reverse('blog:post_data', args = (post_pk, )))


def logout_view(request):
    """Handle requests to blog:logout."""
    logout(request)
    return HttpResponseRedirect(reverse('blog:index'))
