from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user_rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        post_rating = Post.objects.filter(author_id=self).aggregate(pr=Coalesce(Sum('post_rating'), 0))['pr']
        comments_rating = Comment.objects.filter(user_id=self.user).aggregate(cr=Coalesce(Sum('comment_rating'), 0))['cr']
        post_comments_rating = Comment.objects.filter(post_id__author_id=self).aggregate(pcr=Coalesce(Sum('comment_rating'), 0))['pcr']

        self.user_rating = post_rating * 3 + comments_rating + post_comments_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    news = 'NE'
    article = 'AR'

    POST_TIPE = [
        (news, "Новость"),
        (article, 'Статья')
    ]

    post_time_in = models.DateTimeField(auto_now_add=True)
    post_type = models.CharField(max_length=2, choices=POST_TIPE)
    title = models.CharField(max_length=255, default='None')
    post_text = models.TextField(default="Здесь пока никто ничего не написал.")
    post_rating = models.IntegerField(default=0)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        return f'{self.title.title()}: {self.preview()}, Рейтинг новости: {self.post_rating}'

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[:124] + '...'


class Comment(models.Model):
    comm_time_in = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField(default="Комментариев пока нет.")
    comment_rating = models.IntegerField(default=0)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
