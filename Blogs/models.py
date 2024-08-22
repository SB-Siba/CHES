from django.db import models
from ckeditor.fields import RichTextField
from helpers import utils
from django.template.defaultfilters import slugify

class Blogs(models.Model):
    ACCEPTREJECT = (
        ("approved","approved"),
        ("rejected","rejected"),
        ("pending","pending")
    )
    slug = models.SlugField(max_length=255, null=True, blank=True, unique=True)
    title = models.CharField(max_length=255,null=True, blank=True)
    author = models.CharField(max_length=255,null=True, blank=True)
    date = models.DateField()
    content = RichTextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    is_accepted = models.CharField(max_length=10, choices= ACCEPTREJECT, default='pending')

    def save(self, *args, **kwargs):
            if not self.slug:
                self.slug = slugify(self.title)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

 