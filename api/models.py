from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=127)
    text = models.TextField(max_length=2048, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    number_of_views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(max_length=2048)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment-{self.pk}'
