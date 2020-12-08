from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from tinymce.models import HTMLField
from taggit.managers import TaggableManager

# Create your models here.

User = get_user_model()

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='like', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ' : ' + str(self.post)

    class Meta:
       unique_together = ("user", "post")

class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    post_content = HTMLField()
    #post_content = models.TextField()
    #comment_count = models.IntegerField(default=0)
    #view_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    previous_post = models.ForeignKey('self', related_name="previous", on_delete=models.SET_NULL, null=True, blank=True )
    next_post = models.ForeignKey('self', related_name="next", on_delete=models.SET_NULL, null=True, blank=True )
    tags = TaggableManager(blank=True)
    #likes = models.ManyToManyField(User, related_name='blog_posts')
    #slug = models.SlugField(unique=True, max_length=100)
    # slug = models.SlugField(
    #     default='',
    #     editable=False,
    #     max_length=100,
    # )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'pk':self.pk
        })

    def get_update_url(self):
        return reverse('post-update', kwargs={
            'pk':self.pk
        })

    def get_delete_url(self):
        return reverse('post-delete', kwargs={
            'pk':self.pk
        })

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()


    @property
    def like_count(self):
        return Like.objects.filter(post=self).count()
