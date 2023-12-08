from django.shortcuts import render
from .forms import CreatePostForm
from django.shortcuts import render, redirect
from django.urls import reverse


# Create your views here.
def create_post(request, username):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('people:user_detail', kwargs={'username': username}))
    else:
        form = CreatePostForm()
    return render(request, 'blog/create_new_post.html', {'form': form})
