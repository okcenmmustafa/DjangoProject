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

CITY = {
    ('Istanbul','Istanbul'),
    ('Ankara','Ankara'),
    ('Izmir','Izmir'),
}

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields= ('phone', 'adress','city','country','image')
        widgets = {
            'phone' : TextInput(attrs={'class' : 'input','placeholder' : 'phone'}),
            'adress' : TextInput(attrs={'class' : 'input','placeholder' : 'adress'}),
            'city' : Select(attrs={'class' : 'input','placeholder' : 'phone'},choices=CITY),
            'country' : TextInput(attrs={'class' : 'input','placeholder' : 'country'}),
            'image' : FileInput(attrs={'class' : 'input ','placeholder' : 'image'}),
        }