from django import forms
from .models import Post
from django.db import models
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
