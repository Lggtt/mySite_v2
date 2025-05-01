from django.db import models
from django.contrib.auth.models import User


# News Feed
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=20, default='friends')  # or 'public', etc.


# comments
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# Reactions
class Reaction(models.Model):
    post = models.ForeignKey(Post, related_name='reactions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=20, default='like')  # could be 'like', 'love', etc.

    class Meta:
        unique_together = ('post', 'user', 'reaction_type')
