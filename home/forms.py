from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    query = forms.CharField(label='Search' , max_length=100)
    catid = forms.IntegerField()
    cityid = forms.IntegerField()
    priceid = forms.IntegerField()


class SearchForm2(forms.Form):
    query2 = forms.CharField(label='Search2' , max_length=100)
    catid2 = forms.IntegerField()
    cityid2 = forms.IntegerField()
    minbedid = forms.IntegerField()
    districtid = forms.CharField(label='ilce' , max_length=100)
    minbathid = forms.IntegerField()
    minpriceid = forms.IntegerField()
    maxpriceid = forms.IntegerField()
    minareaid = forms.IntegerField()
    maxareaid = forms.IntegerField()



class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30,label='User Name :')
    email = forms.EmailField(max_length=200,label='Email :')
    first_name = forms.CharField(max_length=100 , help_text='First Name',label='First Name :')
    last_name = forms.CharField(max_length=100 , help_text='Last Name',label='Last Name :')

    class Meta:
        model = User
        fields = ('username' , 'email' , 'first_name' , 'last_name' , 'password1' , 'password2' ,)
