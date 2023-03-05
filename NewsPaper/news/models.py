from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorName = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRate = models.SmallIntegerField(default=0)

    def update_rating(self):
        authName = self.authorName.username
        allPostComments = Comment.objects.filter(commentPost__postAuthor__authorName__username=authName)
        allPostCommentsRate = allPostComments.aggregate(allPostCommentsRates=Sum('commentRate'))
        allPostCommentsRateSum = allPostCommentsRate.get('allPostCommentsRates')

        postRate = self.post_set.all().aggregate(postRates=Sum('postRate'))
        postRateSum = postRate.get('postRates')

        authors_comments_rates = self.authorName.comment_set.all().aggregate(au_com_rates=Sum('commentRate'))
        authCommRateSum = authors_comments_rates.get('au_com_rates')

        result_rate = allPostCommentsRateSum + (postRateSum * 3) + authCommRateSum
        self.authorRate = result_rate
        self.save()

        def __str__(self):
            return f'{self.authorName.username}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.name.title()}'


news = 'NEWS'
article = 'ARTC'
post_types = [(news, 'новость'),
              (article, 'статья')]


class Post(models.Model):
    postAuthor = models.ForeignKey(Author, on_delete=models.CASCADE,)
    postType = models.CharField(max_length=4, choices=post_types, default=news)
    postDatetime = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory', related_name='posts',)
    head = models.CharField(max_length=124)
    postText = models.TextField()
    postRate = models.SmallIntegerField(default=0)

    #objects = models.Manager()

    def like(self):
        self.postRate += 1
        self.save()

    def dislike(self):
        self.postRate -= 1
        self.save()

    def preview(self):
        return f'{self.postText[:125]}...'

    def __str__(self):
        return f'{self.head.title()[:18]}: {self.postText[:20]}'

    def get_absolute_url(self):
        return f'/posts/{self.id}'

    def __str__(self):
        return f'{self.get_postType_display()}'


class PostCategory(models.Model):
    postCategory = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryPost = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentTxt = models.TextField()
    commentDatetime = models.DateTimeField(auto_now_add=True)
    commentRate = models.IntegerField(default=0)
    #objects = models.Manager()

    def like(self):
        self.commentRate += 1
        self.save()

    def dislike(self):
        self.commentRate -= 1
        self.save()
