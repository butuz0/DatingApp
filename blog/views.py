from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import CreatePostForm, CreateCommentForm
from django.urls import reverse
from .models import Post


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

    if request.method == 'POST':
        comment_form = CreateCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect(reverse('people:user_detail', kwargs={'username': request.user.username}))

    else:
        comment_form = CreateCommentForm()

    return render(request, 'blog/post_details.html', {'post': post,
                                                      'comment_form': comment_form})


@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    print(f'adding comment to post {post}')
    comment_form = CreateCommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect(reverse('people:user_detail', kwargs={'username': request.user.username}))


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
