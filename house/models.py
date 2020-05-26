import sys

from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
# Create your models here.
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS = (
        ('True' , 'Evet') ,
        ('False' , 'Hayır') ,
    )

    title = models.CharField(max_length=90)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    listeleme = models.IntegerField(default=0)
    image = models.ImageField(blank=True , upload_to='images/')
    status = models.CharField(max_length=10 , choices=STATUS)
    slug = models.SlugField(null=False , unique=True)
    parent = TreeForeignKey('self' , blank=True , null=True , related_name='children' , on_delete=models.CASCADE)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '/'.join(full_path[::-1])
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail' , kwargs={'slug': self.slug})

class housefav(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    house=models.ForeignKey("House",on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class House(models.Model):
    STATUS = (
        ('True' , 'Evet') ,
        ('False' , 'Hayır') ,

    )
    Kredi = (
        ('True' , 'Evet') ,
        ('False' , 'Hayır') ,

    )
    takas = (
        ('True' , 'Evet') ,
        ('False' , 'Hayır') ,

    )
    Esya = (
        ('Esyali' , 'Esyali') ,
        ('Esyasiz' , 'Esyasiz') ,

    )
    kullanim = (
        ('Bos' , 'Bos') ,
        ('Dolu' , 'Dolu') ,
    )
    kimden = (
        ('Sahibinden' , 'Sahibinden') ,
        ('Emlak' , 'Emlak') ,
    )
    cephe = (
        ('Güney' , 'Güney') ,
        ('Kuzey' , 'Kuzey') ,
    )
    binatipler = (
        ('Kerpiç Bina' , 'Kerpiç Bina') ,
        ('Ahşap Bina' , 'Ahşap Bina') ,
        ('Yarı Kagir Bina' , 'Yarı Kagir Bina') ,
        ('Kagir Bina' , 'Kagir Bina') ,
        ('Betonarme Bina' , 'Betonarme Bina') ,
        ('Çelik  Bina' , 'Çelik  Bina') ,
    )
    tapu = (
        ('Kat mülkiyetli tapu' , 'Kat mülkiyetli tapu') ,
        ('Kat irtifaklı tapu' , 'Kat irtifaklı tapu') ,
        ('Hisseli tapu' , 'Hisseli tapu') ,

    )
    Cities = (
        ('1' , 'Adana') ,
        ('2' , 'Adıyaman') ,
        ('3' , 'Afyonkarahisar') ,
        ('4' , 'Ağrı ') ,
        ('5' , 'Amasya ') ,
        ('6' , 'Ankara ') ,
        ('7' , 'Antalya ') ,
        ('8' , 'Artvin ') ,
        ('9' , 'Aydın ') ,
        ('10' , 'Balıkesir') ,
        ('11' , 'Bilecik ') ,
        ('12' , 'Bingöl ') ,
        ('13' , 'Bitlis ') ,
        ('14' , 'Bolu ') ,
        ('15' , 'Burdur ') ,
        ('16' , 'Bursa ') ,
        ('17' , 'Çanakkale') ,
        ('18' , 'Çankırı ') ,
        ('19' , 'Çorum ') ,
        ('20' , 'Denizli ') ,
        ('21' , 'Diyarbakır ') ,
        ('22' , 'Edirne ') ,
        ('23' , 'Elazığ ') ,
        ('24' , 'Erzincan ') ,
        ('25' , 'Erzurum ') ,
        ('26' , 'Eskişehir ') ,
        ('27' , 'Gaziantep ') ,
        ('28' , 'Giresun ') ,
        ('29' , 'Gümüşhane ') ,
        ('30' , 'Hakkâri ') ,
        ('31' , 'Hatay ') ,
        ('32' , 'Isparta ') ,
        ('33' , 'Mersin ') ,
        ('34' , 'İstanbul ') ,
        ('35' , 'İzmir ') ,
        ('59' , 'Tekirdağ') ,
        ('60' , 'Tokat ') ,
        ('61' , 'Trabzon ') ,
        ('62' , 'Tunceli ') ,
        ('63' , 'Şanlıurfa ') ,
        ('64' , 'Uşak ') ,
        ('65' , 'Van ') ,
        ('66' , 'Yozgat') ,
        ('67' , 'Zonguldak') ,
        ('68' , 'Aksaray ') ,
        ('69' , 'Bayburt ') ,
        ('70' , 'Karaman ') ,
        ('71' , 'Kırıkkale ') ,
        ('72' , 'Batman ') ,
        ('73' , 'Şırnak ') ,
        ('74' , 'Bartın ') ,
        ('75' , 'Ardahan ') ,
        ('76' , 'Iğdır ') ,
        ('77' , 'Yalova ') ,
        ('78' , 'Karabük ') ,
        ('79' , 'Kilis ') ,
        ('80' , 'Osmaniye') ,
        ('81' , 'Düzce ') ,
        ('82','Diğer')
    )

    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    userOwner = models.ForeignKey(User , on_delete=models.CASCADE , default=0)
    title = models.CharField(max_length=100)
    keywords = models.CharField(max_length=255)
    kimden = models.CharField(max_length=20,choices=kimden,default="Sahibinden")
    image = models.ImageField(blank=True , upload_to='images/')
    price = models.IntegerField(blank=True , default=0)
    aidat = models.IntegerField(blank=True , default=0)
    buildTime = models.IntegerField(blank=True , default=0)
    kat = models.IntegerField(blank=True,default=0)
    isinmatip = models.CharField(max_length=255,blank=True)
    katsayisi = models.IntegerField(blank=True,default=0)
    KrediUygun = models.CharField(max_length=10 , choices=Kredi,default="Hayır")
    esyaDurum = models.CharField(max_length=10 , choices=Esya,default="Esyasiz")
    yapiTipi = models.CharField(max_length=25, choices=binatipler,default="Betonarme Bina")
    kullanimDurumu = models.CharField(max_length=10,choices=kullanim,default="bos")
    tapuDurumu = models.CharField(max_length=30,choices=tapu,default="Kat irtifaklı tapu")
    takas = models.CharField(max_length=10,choices=takas,default="Hayir")
    cephe = models.CharField(max_length=20,choices=cephe,default="Güney")
    description = models.CharField(max_length=255,blank=True)
    area = models.IntegerField(blank=True , default=0)
    bedroom = models.IntegerField(blank=True , default=0)
    bathroom = models.IntegerField(blank=True , default=0)
    garage = models.IntegerField(blank=True , default=0)
    slug = models.SlugField(null=False , unique=True)
    locationDetail = models.CharField(max_length=150 , default="-")
    city = models.CharField(max_length=50 , choices=Cities)
    district = models.CharField(max_length=70 , default="-")
    detail = RichTextUploadingField()
    status = models.CharField(max_length=10 , choices=STATUS)
    favorite= models.ManyToManyField(User,related_name='favorite',blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height=50"/>'.format(self.image.url))
        image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('house_detail' , kwargs={'slug': self.slug})




class Images(models.Model):
    house = models.ForeignKey(House , on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image = models.ImageField(blank=True , upload_to='images/')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height=50"/>'.format(self.image.url))
        image_tag.short_description = 'Image'

class HouseImageForm(ModelForm):
    class Meta:
        model = Images
        fields = ['title','image']



class Comment(models.Model):
    STATUS = (
        ('New' , 'Yeni') ,
        ('True' , 'Evet') ,
        ('False' , 'Hayır') ,
    )
    house = models.ForeignKey(House , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    subject = models.CharField(max_length=50 , blank=True)
    comment = models.TextField(max_length=255 , blank=True)
    rate = models.IntegerField(blank=True)
    status = models.CharField(max_length=10 , choices=STATUS , default='New')
    ip = models.CharField(blank=True , max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject' , 'comment' , 'rate']

class CImages(models.Model):
    house=models.ForeignKey(House,on_delete=models.CASCADE)
    title=models.CharField(max_length=50,blank=True)
    image=models.ImageField(blank=True,upload_to='images/')
    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src"{}" height="50"/>'.format(self.image.url))
    image_tag.short_description='Image'
