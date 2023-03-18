from django.contrib import admin
from .models import Post, Category, Comment
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['postAuthor', 'postType', 'head', 'postRate', 'postText',]  # "category__name"]
    #list_display = [field.name for field in Post._meta.get_fields()]
    list_filter = ['postAuthor__authorName__username', 'postType', 'category', 'head', 'postRate']  # simple filters
    search_fields = ["postAuthor__authorName__username", 'postType', 'category__name', 'head', 'postRate']  # advanced filters
    #search_fields = ['postType', 'category__name', 'head', 'postRate']  # advanced filters

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', "subscribers__username")  # simple filters
    search_fields = ('name', "subscribers__username")  # advanced filters


class CommentAdmin(admin.ModelAdmin):
    list_display = ('commentUser', 'commentTxt', 'commentDatetime', 'commentRate')
    list_filter = ('commentUser__username', 'commentTxt', 'commentDatetime', 'commentRate')  # simple filters
    search_fields = ('commentUser__username', 'commentTxt', 'commentDatetime', 'commentRate')  # advanced filters


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
