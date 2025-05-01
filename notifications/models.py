# In posts/views.py after a comment is created
from notifications.models import Notification
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


#Notifications alert users about new friends, comments, likes, or messages.
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)


# In posts/views.py after a comment is created
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        comment_content = request.POST.get('content')
        comment = Comment.objects.create(post=post, author=request.user, content=comment_content)
        # Create a notification for the post author
        Notification.objects.create(
            user=post.author,
            text=f"{request.user.username} commented on your post."
        )
        return redirect('posts:detail', post_id=post.id)


#View to see notifications
@login_required
def notifications_view(request):
    user_notifications = request.user.notifications.filter(read=False).order_by('-created_at')
    return render(request, 'notifications/list.html', {'notifications': user_notifications})


#Mark as read logic
@login_required
def mark_notification_read(request, notification_id):
    notif = Notification.objects.get(id=notification_id, user=request.user)
    notif.read = True
    notif.save()
    return redirect('notifications:list')
