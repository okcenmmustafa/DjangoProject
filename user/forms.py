from django import forms

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput , EmailInput ,  Select , FileInput

from home.models import UserProfile


class UserUpdateForm(UserChangeForm):
    class Meta:
        model=User
        fields ={'username','first_name','last_name','email'}
        widgets={

            'username' : TextInput(attrs={'class': 'input','placeholder':'username'}),
            'email': EmailInput(attrs={'class': 'input' , 'placeholder': 'email'}) ,
            'last_name': TextInput(attrs={'class': 'input','placeholder' : 'last_name'}),
            'first_name': TextInput(attrs={'class': 'input' , 'placeholder': 'first_name'}),

        }


CITY = (
    ('Adana' , 'Adana') ,
    ('Adıyaman' , 'Adıyaman') ,
    ('Afyonkarahisar' , 'Afyonkarahisar') ,
    ('Ağrı' , 'Ağrı ') ,
    ('Amasya' , 'Amasya ') ,
    ('Ankara' , 'Ankara ') ,
    ('Antalya' , 'Antalya ') ,
    ('Artvin' , 'Artvin ') ,
    ('Aydın' , 'Aydın ') ,
    ('Balıkesir' , 'Balıkesir') ,
    ('Bilecik' , 'Bilecik ') ,
    ('Bingöl' , 'Bingöl ') ,
    ('Bitlis' , 'Bitlis ') ,
    ('Bolu' , 'Bolu ') ,
    ('Burdur' , 'Burdur ') ,
    ('Bursa' , 'Bursa ') ,
    ('Çanakkale' , 'Çanakkale') ,
    ('Çankırı' , 'Çankırı ') ,
    ('Çorum' , 'Çorum ') ,
    ('Denizli' , 'Denizli ') ,
    ('Diyarbakır' , 'Diyarbakır ') ,
    ('Edirne' , 'Edirne ') ,
    ('Elazığ' , 'Elazığ ') ,
    ('Erzincan' , 'Erzincan ') ,
    ('Erzurum' , 'Erzurum ') ,
    ('Eskişehir' , 'Eskişehir ') ,
    ('Gaziantep' , 'Gaziantep ') ,
    ('Giresun' , 'Giresun ') ,
    ('Gümüşhane' , 'Gümüşhane ') ,
    ('Hakkâri' , 'Hakkâri ') ,
    ('Hatay' , 'Hatay ') ,
    ('Isparta' , 'Isparta ') ,
    ('Mersin' , 'Mersin ') ,
    ('Istanbul' , 'İstanbul ') ,
    ('İzmir' , 'İzmir ') ,
    ('Tekirdağ' , 'Tekirdağ') ,
    ('Tokat' , 'Tokat ') ,
    ('Trabzon' , 'Trabzon ') ,
    ('Tunceli' , 'Tunceli ') ,
    ('Şanlıurfa' , 'Şanlıurfa ') ,
    ('Uşak' , 'Uşak ') ,
    ('Van' , 'Van ') ,
    ('Yozgat' , 'Yozgat') ,
    ('Zonguldak' , 'Zonguldak') ,
    ('Aksaray' , 'Aksaray ') ,
    ('Bayburt' , 'Bayburt ') ,
    ('Karaman' , 'Karaman ') ,
    ('Kırıkkale' , 'Kırıkkale ') ,
    ('Batman' , 'Batman ') ,
    ('Şırnak' , 'Şırnak ') ,
    ('Bartın' , 'Bartın ') ,
    ('Ardahan' , 'Ardahan ') ,
    ('Iğdır' , 'Iğdır ') ,
    ('Yalova' , 'Yalova ') ,
    ('Karabük' , 'Karabük ') ,
    ('Kilis' , 'Kilis ') ,
    ('Osmaniye' , 'Osmaniye') ,
    ('Düzce' , 'Düzce ') ,
    ('Diğer' , 'Diğer ') ,
)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields= ('phone', 'adress','city','country','image')
        widgets = {
            'phone' : TextInput(attrs={'class' : 'input','placeholder' : 'phone'}),
            'adress' : TextInput(attrs={'class' : 'input','placeholder' : 'adress'}),
            'city' : Select(attrs={'class' : 'input','placeholder' : 'phone'},choices=CITY),
            'country' : TextInput(attrs={'class' : 'input','placeholder' : 'country'}),
            'image' : FileInput(attrs={'class' : 'input ','placeholder' : 'image','id':'resim'}),
        }