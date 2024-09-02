from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from post.models import Tag, Stream, Follow, Post, likes
from post.forms import  NewPostForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from userauths.models import Profile
from comment.models import Comment
from comment.forms import CommentForm
from django.contrib.auth.models import User
from django.db import transaction
# Create your views here.
@login_required
def index(request):
    user = request.user
    all_users = User.objects.all()
    posts = Stream.objects.filter(user=user)
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    group_ids = []


    for post in posts:
        group_ids.append(post.post_id)
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    context = {
        'post_items':post_items,
        'all_users':all_users,
        'follow_status':follow_status

    }
    return render(request, 'index.html', context)

@login_required
def NewPost(request):
    user = request.user.id
    tags_objs = []

    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES) 
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tag')
            tags_list = list(tag_form.split(','))

            try:
                with transaction.atomic():
                    for tag in tags_list:
                        t, created = Tag.objects.get_or_create(title=tag)
                        tags_objs.append(t)

                    p = Post.objects.create(picture=picture, caption=caption, user_id=user)
                    p.tag.set(tags_objs)
                    p.save()

                    return redirect('index')
            except IntegrityError:
                form.add_error(None, "A post with similar data already exists.")

    else:
        form = NewPostForm()

    context = {
        'form': form
    }
    return render(request, 'newpost.html', context)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      


def PostDetail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    #comment
    comments = Comment.objects.filter(post=post).order_by("-date")

    #commentform
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES) 
        if form.is_valid():

            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            
            return HttpResponseRedirect(reverse("post-details", args=[post_id]))
    else:
        form = CommentForm()
    context = {
        'form':form,
         'comments':comments,
        'post':post
    }
    return render(request, 'post-details.html', context)

@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = likes.objects.filter(user=user, post=post).count()
    if not liked:
        liked = likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        liked = likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
    post.likes = current_likes
    post.save()
    return redirect('/post')

@login_required
def favourite(request, post_id):
    user = request.user
    profile = Profile.objects.get(user=user)
    post = Post.objects.get(id=post_id)

    if profile.favourite.filter(id=post_id).exists():
     profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return HttpResponseRedirect(reverse('post-details', args=[post_id]))
