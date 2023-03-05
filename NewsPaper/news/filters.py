from django_filters import FilterSet
#from django import forms
#from django.db import models
#import django_filters as filters
#from django.utils.translation import gettext_lazy as _
from .models import Post

class PostFilter(FilterSet):

    class Meta:
        model = Post
        fields = {
            'postDatetime': ['gt'],
            'head': ['icontains',],
            'postAuthor__authorName__username': ['icontains'],
        }

