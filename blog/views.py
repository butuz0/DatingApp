from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from .forms import CreatePostForm, CreateCommentForm
from .models import Post, Comment
from .redis_utils import add_comment_like, remove_comment_like, get_comment_likes_count, has_liked_comment


# Create your views here.
@login_required
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('people:user_detail', kwargs={'username': request.user.username}))
    else:
        form = CreatePostForm()
    return render(request, 'blog/create_new_post.html', {'form': form})


@login_required
def edit_blog(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/edit_blog.html', {'posts': posts})


@login_required
def get_post(request, post_id):
    post = Post.objects.get(id=post_id)

    comments = Comment.objects.filter(post=post_id)
    for comment in comments:
        comment.likes_amount = get_comment_likes_count(comment.id)
        comment.has_liked_comment = has_liked_comment(request.user.id, comment.id)

    comment_form = CreateCommentForm()
    return render(request, 'blog/post_details.html', {'post': post,
                                                      'comments': comments,
                                                      'comment_form': comment_form})


@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    comment_form = CreateCommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect(reverse('blog:get_post', kwargs={'post_id': post_id}))


@login_required
def delete_comment(request, post_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect(reverse('blog:get_post', kwargs={'post_id': post_id}))
    else:
        return render(request, 'blog/delete_comment.html', {'comment': comment})


@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('people:user_detail', kwargs={'username': request.user.username}))
    else:
        form = CreatePostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect(reverse('blog:edit_blog'))
    else:
        return render(request, 'blog/delete_post.html', {'post': post})


@login_required
def like_comment(request):
    comment_id = request.POST.get('id')
    action = request.POST.get('action')

    if comment_id and action:
        if action == 'comment_like':
            add_comment_like(request.user.id, comment_id)
        else:
            remove_comment_like(request.user.id, comment_id)
        return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'error'})
