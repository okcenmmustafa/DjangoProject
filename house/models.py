from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )

    title = models.CharField(max_length=90)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False,unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k=self.parent
        while k is not None:
            full_path.append(k.title)
            k=k.parent
        return '/'.join(full_path[::-1])
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug' : self.slug})


class House(models.Model):
    STATUS = (
        ('1+0 Studio', '1+0 Studio'),
        ('1+1', '1+1'),
        ('2+1', '2+1'),
        ('3+1', '3+1'),
        ('4+1', '4+1'),
        ('5+1', '5  +1'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.FloatField()
    slug = models.SlugField(null=False, unique=True)
    location = models.CharField(max_length=255)
    detail = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height=50"/>'.format(self.image.url))
        image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('house_detail', kwargs={'slug' : self.slug})

class Images(models.Model):
    house=models.ForeignKey(House,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    image=models.ImageField(blank=True,upload_to='images/')

    def __str__(self):
        return self.title
    def image_tag(self):
        return mark_safe('<img src="{}" height=50"/>'.format(self.image.url))
        image_tag.short_description = 'Image'
