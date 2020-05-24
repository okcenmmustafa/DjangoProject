from ckeditor.widgets import CKEditorWidget
from django.forms import ModelForm , NumberInput , SlugField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.db import models

from house.models import House , Category
from django.forms import TextInput , EmailInput ,  Select , FileInput

class Menu(MPTTModel):
    STATUS=(
        ('True','Evet'),
        ('False','Hayır')
    )
    prent= TreeForeignKey('self', blank=True,null=True,related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=255)
    status = models.CharField(max_length=10 , choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by=['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '/'.join(full_path[::-1])
        return self.title

class HouseForm(ModelForm):
    class Meta:
        model = House
        fields=['title','slug','description','keywords','category','image','price','buildTime','area','bedroom','bathroom','garage','city','locationDetail','district','detail']

        widgets={
            'title' : TextInput(attrs={'placeholder' : 'title','class': 'form-control'}),
            'slug' : TextInput(attrs={'placeholder' : 'slug','class': 'form-control'},),
            'description' : TextInput(attrs={'placeholder' : 'description','class': 'form-control'}),
            'keywords' : TextInput(attrs={'placeholder' : 'keywords','class': 'form-control'}),
            'category' : Select(attrs={'placeholder' : 'category','class': 'form-control'}),
            'price' : NumberInput(attrs={'placeholder' : 'price','class': 'form-control','onclick':'commas(self)'},),
            'buildTime' : NumberInput(attrs={'placeholder' : 'buildTime','class': 'form-control'}),
            'area' : NumberInput(attrs={'placeholder' : 'area','class': 'form-control'}),
            'bedroom' : NumberInput(attrs={'placeholder' : 'bedroom','class': 'form-control'}),
            'bathroom' : NumberInput(attrs={'placeholder' : 'bathroom','class': 'form-control'}),
            'garage' : NumberInput(attrs={'placeholder' : 'garage','class': 'form-control'}),
            'city' : Select(attrs={'placeholder' : 'city','class': 'form-control'}),
            'district' : TextInput(attrs={'placeholder' : 'district','class': 'form-control'}),
            'locationDetail' : TextInput(attrs={'placeholder' : 'locationDetail','class': 'form-control'}),
            'image' : FileInput(attrs={'placeholder' : 'image','class': 'form-control'}),
            'detail' :CKEditorWidget(),
        }




