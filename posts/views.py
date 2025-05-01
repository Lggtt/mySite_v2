from django.contrib.auth.decorators import login_required
from friends.models import Friendship, are_friends
from .forms import PostForm
from .models import Post
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# feed view
@login_required
def feed_view(request):
    # Get all users the current user is friends with or follows
    friend_ids = [f.to_user.id for f in request.user.following.all() if are_friends(request.user, f.to_user)]
    # Include the user themselves
    friend_ids.append(request.user.id)
    # Filter posts by these user IDs and privacy settings
    posts = Post.objects.filter(author_id__in=friend_ids).order_by('-created_at')
    return render(request, 'posts/feed.html', {'posts': posts})


#post creation view
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('posts:feed')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


#editing posts
@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:feed')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form})
