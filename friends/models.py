from django.db import models
from django.contrib.auth.models import User


# Friendship/Follower System
class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')


def are_friends(user1, user2):
    return Friendship.objects.filter(from_user=user1, to_user=user2).exists() and \
        Friendship.objects.filter(from_user=user2, to_user=user1).exists()
