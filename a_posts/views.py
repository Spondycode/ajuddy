from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
from bs4 import BeautifulSoup
from .models import *
from .forms import *
import requests
from django.contrib import messages

def home_view(request, tag=None):
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        posts = Post.objects.all()

    context = {'posts' :posts, 'tag': tag}
    return render(request, 'a_posts/home.html', context)




@login_required
def post_create_view(request):
    form = PostCreateForm()

    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            website = requests.get(form.data['url'])
            sourcecode = BeautifulSoup(website.text, 'html.parser')

            find_image = sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
            try:   
                image = find_image[0]['content']
            except:
                messages.error(request, 'Requested image is not on Flickr!')
                return redirect('post-create')


            image = find_image[0]['content']
            post.image = find_image

            find_title = sourcecode.select('h1.photo-title')
            title = find_title[0].text.strip()
            post.title = title


            find_artist = sourcecode.select('a.owner-name')
            artist = find_artist[0].text.strip()
            post.artist = artist


            post.author = request.user

            post.save()
            form.save_m2m()
            return redirect('home')

    context = {'form' :form}
    return render(request, 'a_posts/post_create.html', context)


@login_required
def post_delete_view(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)

    if request.method == "POST":
        post.delete()
        messages.success(request, 'The post was deleted...')
        return redirect('home')

    context = {'post': post}
    return render(request, 'a_posts/post_delete.html', context)


@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    form = PostEditForm(instance=post)

    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid:
            form.save()
            messages.success(request, 'The post was edited...')
            return redirect('home')

    context = {'post': post, 'form': form}
    return render(request, 'a_posts/post_edit.html', context)


def post_page_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    commentform = CommentCreateForm()
    replyform = ReplyCreateForm

    if request.htmx:
        if 'top' in request.GET:
            # comments = post.comments.filter(likes__isnull=False).distinct()
            comments = post.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        else:
            comments = post.comments.all()
        context = {'comments': comments, 'replyform': replyform}
        return render(request, 'snippets/loop_postpage_comments.html', context)

    context = {
        'post': post,
        'commentform': commentform,
        'replyform': replyform,
    }
    return render(request, 'a_posts/post_page.html', context)

@login_required
def comment_sent(request, pk):
    post = get_object_or_404(Post, id=pk)
    replyform = ReplyCreateForm()


    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()

    context = {'comment': comment, 'post': post, 'replyform': replyform}
    return render(request, 'snippets/add_comment.html', context)



@login_required
def comment_delete_view(request, pk):
    post = get_object_or_404(Comment, id=pk, author=request.user)

    if request.method == "POST":
        post.delete()
        messages.success(request, 'The comment was deleted...')
        return redirect('post', post.parent_post.id)

    context = {'comment': post}
    return render(request, 'a_posts/comment_delete.html', context)



@login_required
def reply_sent(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    replyform = ReplyCreateForm()

    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid:
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()

    context = {'comment': comment, 'reply': reply, 'replyform': replyform}
    return render(request, 'snippets/add_reply.html', context)



@login_required
def reply_delete_view(request, pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)

    if request.method == "POST":
        reply.delete()
        messages.success(request, 'The reply was deleted...')
        return redirect('post', reply.parent_comment.parent_post.id)

    context = {'reply': reply}
    return render(request, 'a_posts/reply_delete.html', context)



def like_toggle(model):
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            post = get_object_or_404(model, id=kwargs.get('pk'))
            user_exist = post.likes.filter(username=request.user.username).exists()

            if post.author != request.user:
                if user_exist:
                    post.likes.remove(request.user)
                else:
                    post.likes.add(request.user)

            return func(request, post)
        return wrapper
    return inner_func


@login_required
@like_toggle(Post)
def like_post(request, post):
    context = {'post': post}
    return render(request, 'snippets/likes.html', context) 


@login_required
@like_toggle(Comment)
def like_comment(request, post):
    context = {'comment': post}
    return render(request, 'snippets/likes_comment.html', context) 


@login_required
@like_toggle(Reply)
def like_reply(request, post):
    context = {'reply': post}
    return render(request, 'snippets/likes_reply.html', context) 
