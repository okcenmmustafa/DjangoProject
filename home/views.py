import json

from django.contrib import messages
from django.contrib.auth import logout , authenticate , login

from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template import context

import house
from home.forms import SearchForm , SignUpForm
from home.models import Setting , ContactFormMessage , ContactFormu , UserProfile
from house.models import House , Category , Images


def index(request):
    setting= Setting.objects.get(pk=1)
    sliderdata =House.objects.all()[:4]
    category=Category.objects.all()
    yeniEklenenler=House.objects.all().order_by('-id')[:4]
    context={'setting':setting,
             'category':category,
             'page':'home',
             'yeniEklenenler':yeniEklenenler,
             'sliderdata':sliderdata}

    return render(request, "index.html",context)

def hakkimizda(request):
    setting= Setting.objects.get(pk=1)
    context={'setting':setting,'page':'hakkimizda'}
    return render(request, "hakkimizda.html",context)


def ilanlar(request):
    category = Category.objects.all()
    houses = House.objects.all()
    context={'category':category,
             'houses':houses}
    return render(request,"ilanlar.html",context)


def category_ilanlar(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    houses = House.objects.filter(category_id=id)

    context={'houses': houses,
             'category': category,
             'categorydata': categorydata,
             }
    return render(request, "ilanlar.html", context)


def iletisim(request):
    form = ContactFormu()
    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # model ile baglantı kurma
            data.name = form.cleaned_data['name']  # formdan bilgi alma
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()  # veritabanına kaydetme
            messages.success(request, 'Mesajınız baaşarı ile gönderilmiştir.Teşekkür ederiz')
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)
    form =ContactFormu()
    context = {'setting': setting, 'form': form}
    return render(request,  'iletisim.html', context)


def UrunSayfasi(request,id,slug):
    category = Category.objects.all()
    house = House.objects.get(pk=id)
    images = Images.objects.filter(house_id=id)
    context={'category':category,
             'house':house,
             'images':images,
                }

    mesaj="Ev",id,"/",slug
    return render(request,'singleEvDetay.html',context)

def house_search(request):
    if request.method =='POST':
        form=SearchForm(request.POST)
        if form.is_valid():
            category=Category.objects.all()
            query=form.cleaned_data['query']
            catid=form.cleaned_data['catid']
            if catid==0:
                houses=House.objects.filter(title__icontains=query)
            else:
                houses = House.objects.filter(location__icontains=query,category_id=catid)


            context ={'houses':houses,
                      'category':category,
            }
            return render(request,'homeSearch.html',context)

def house_search_auto(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    house = House.objects.filter(location__icontains=q)
    results = []
    for rs in house:
      house_json = {}
      house_json = rs.location
      results.append(house_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username=username , password=password)
        if user is not None:
            login(request , user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Kullanıcı adı veya şifre yanlış!")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {
               'category': category ,
               }
    return render(request , 'login.html' , context)

def signup_view(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request , username=username , password=password)
            login(request,user)
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image='images/user.png'
            data.save()
            return HttpResponseRedirect('/')
    form = SignUpForm()
    category = Category.objects.all()
    context = {
        'category': category ,
        'form' : form,
    }
    return render(request , 'signup.html' , context)