from django.db import models

# Create your models here.

from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = "draft", "Chernovoy"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name="posts")
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.ManyToManyField(Tag,related_name="posts",blank=True)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    content = models.TextField()
    parent = models.ForeignKey("self",on_delete=models.CASCADE,null=True,blank=True,related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.post.title}"


class PostReaction(models.Model):

    class Reaction(models.TextChoices):
        LIKE = "like", "Like"
        DISLIKE = "dislike", "Dislike"
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="reactions")
    reaction = models.CharField(max_length=10,choices=Reaction.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.reaction}"