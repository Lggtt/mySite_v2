from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect

# Create your models here.
# Profile Creation and Editing
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # Add more fields as needed, e.g., location, date_of_birth, etc.

    def __str__(self):
        return self.user.username


# Signals to create/update Profile automatically


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


# Add fields to Profile for privacy controls (e.g., who can see your profile, posts, etc.).
PRIVACY_CHOICES = [
    ('public', 'Public'),
    ('friends', 'Friends Only'),
    ('private', 'Private'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    profile_visibility = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='friends')

    # ...


def view_profile(request, username):
    profile_user = User.objects.get(username=username)
    profile = profile_user.profile

    # Check privacy
    if profile.profile_visibility == 'private' and request.user != profile_user:
        # Deny or show a limited view
        return render(request, 'accounts/private_profile.html')
    elif profile.profile_visibility == 'friends':
        # Check if request.user is a friend
        if not are_friends(request.user, profile_user):
            return render(request, 'accounts/private_profile.html')

    # If public or allowed friend, show full profile
    return render(request, 'accounts/profile.html', {'profile': profile})
