from django.db import models
from django.contrib.auth.admin import User
from django.db.models import Sum
from django.urls import reverse
from datetime import datetime



# Create your models here.


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)

    def __str__(self):
        return str(self.author_user)


    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating_article'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.author_user.comment_set.aggregate(commentRating=Sum('rating_comment'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.rating_author = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    topic = models.CharField(max_length=64, unique=True)
    subscribers=models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.topic

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    TYPES = [
        ('AR', 'Статья'),
        ('NW', 'Новость')
    ]
    type = models.CharField(max_length=2,
                            choices=TYPES,
                            default='AR')

    time_in = models.DateTimeField(auto_now_add=True)
    topics = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=64)
    text = models.TextField()
    rating_article = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


    def like(self):
        self.rating_article += 1
        self.save()

    def dislike(self):
        self.rating_article -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    time_in_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()




# Create your models here.
