from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author (models.Model):
    userAuthor = models.OneToOneField(User, on_delete = models.CASCADE)
    ratingAuthor = models.IntegerField(default = 0)

    def update_rating(self):
        postRat = self.post_set.all().aggregate(postRating=Sum('ratingPost'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.userAuthor.comment_set.all().aggregate(commentRating=Sum('ratingComment'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()
    
    def __str__(self):
        return f'{self.userAuthor}'

class Category (models.Model):
    NameCategory = models.CharField(max_length = 64, unique = True)
    subscribers = models.ManyToManyField(User, blank=True)

    def subscribe(self):
        pass

    def __str__(self):
        return f'{self.NameCategory}'

class Post (models.Model):
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    article = 'AR'
    new = 'NW'
    POSTS = [
        (article, 'Статья'),
        (new, 'Новость'),
    ]
    post = models.CharField(max_length = 2, choices = POSTS, default = new)
    datatime = models.DateTimeField(auto_now_add = True)
    data = models.DateField (auto_now_add = True)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max_length = 150, default = '')
    text = models.TextField(default = '')
    ratingPost = models.IntegerField(default = 0)

    def like(self):
        self.ratingPost += 1
        self.save()

    def dislike(self):
        self.ratingPost -= 1
        self.save()
    
    def preview(self):
        return self.text[0:123] + '...'
    
    def __str__(self):
        return f'{self.title} {self.datatime}'
    
    def get_absolute_url(self):   
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его



class PostCategory (models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)

class Comment (models.Model):
    postComment = models.ForeignKey(Post, on_delete = models.CASCADE)
    userComment = models.ForeignKey(User, on_delete = models.CASCADE)
    textComment = models.TextField(default = '')
    datatime = models.DateTimeField(auto_now_add = True)
    ratingComment = models.IntegerField(default = 0)

    def like(self):
        self.ratingComment += 1
        self.save()

    def dislike(self):
        self.ratingComment -= 1
        self.save()