from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


# Create your models here.
from django.forms import ModelForm, TextInput, Textarea
from django.utils.safestring import mark_safe


class Setting(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    adress = models.CharField(blank=True, max_length=150)
    phone = models.CharField(blank=True, max_length=15)
    fax = models.CharField(blank=True, max_length=15)
    email = models.CharField(blank=True, max_length=50)
    smtserver = models.CharField(blank=True,max_length=20)
    smtemail = models.CharField(blank=True,max_length=20)
    smtpassword = models.CharField(blank=True,max_length=10)
    smtpport = models.CharField(blank=True, max_length=5)
    icon = models.ImageField(blank=True, upload_to='images/')
    facebook = models.CharField(blank=True,max_length=50)
    instagram = models.CharField(blank=True,max_length=50)
    twitter = models.CharField(blank=True,max_length=50)
    twitter = models.CharField(blank=True,max_length=50)
    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height=50"/>'.format(self.icon.url))
        image_tag.short_description = 'Image'


class ContactFormMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed','Closed')
    )

    name = models.CharField(blank=True,max_length=20)
    email = models.CharField(blank=True, max_length=50)
    icon = models.ImageField(blank=True, upload_to='images/')
    subject = models.CharField(blank=True,max_length=50)
    message = models.CharField(blank=True,max_length=255)
    ip = models.CharField(blank=True,max_length=50)
    note = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS,default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class ContactFormu(ModelForm):
    class Meta:
        model=ContactFormMessage
        fields = ['name','email','subject','message']
        widgets ={
            'name' : TextInput(attrs={'class': 'input','placeholder':'İsim Soyisim'}),
            'subject' : TextInput(attrs={'class': 'input','placeholder':'Konu'}),
            'email' : TextInput(attrs={'class': 'input','placeholder':'Email adresi'}),
            'message' : Textarea(attrs={'class': 'input','placeholder':'Mesajınız','rows':'5'}),


        }