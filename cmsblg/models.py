from django.conf import settings
from django.db import models
from multiselectfield import MultiSelectField
from auth_user.models import User
from cmscore.models import AlbumPhoto
import os
import random
from random import choice
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

# Create your models here.
def get_existing_file_name(instance, filename):
    """
    Returns the filename with a suffix (e.g. "_1") if a file with the same name
    already exists in the media root directory.
    """
    path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(path):
        name, ext = os.path.splitext(filename)
        i = 1
        while os.path.exists(os.path.join(settings.MEDIA_ROOT, f"{name}_{i}{ext}")):
            i += 1
        # Check if the file with the original filename exists
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, instance.image.name)):
            return instance.image.name
        return f"{name}_{i}{ext}"
    return filename

class Category(models.Model):
    # blgcat_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    caption = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Categories'
        # managed = False
        # db_table = 'cmsblg_category'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/' % self.slug
    
    def post_count(self):
        return self.posts.count()

class Post(models.Model):
    ACTIVE = 'active'
    DRAFT = 'draft'

    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (DRAFT, 'Draft')
    )

    author = models.ForeignKey(User, null=True, blank=True, related_name='posts', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    intro = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=ACTIVE)
    image = models.ImageField(upload_to='post_images/', verbose_name='Image', blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/%s/' % (self.category.slug, self.slug)

class Comment(models.Model):
    name = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    # created_date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

    @property
    def is_parent(self):
        return not self.parent
    
    class Meta:
        ordering = ['-created_at']
        # managed = False
        # db_table = 'cmsblg_comment'

class Fact(models.Model):
    # faq_id = models.AutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField()
    img = models.ImageField(upload_to='Fact', blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_by = models.CharField(max_length=255, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
    #     managed = False
        db_table = 'cmsblg_faq'

    def __str__(self):
        return self.question

class PostImages(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE, null=True, blank=True)
    images = models.ImageField(upload_to='post_images/', verbose_name='Image', blank=True)

    def __str__(self):
        return self.images.name

