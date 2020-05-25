import json
from random import random


from django.contrib import messages
from django.contrib.auth import logout , authenticate , login

from django.db.models import QuerySet
from django.http import HttpResponse , HttpResponseRedirect
from django.shortcuts import render , get_object_or_404

# Create your views here.
from django.template import context

import house
from home.forms import SearchForm , SignUpForm , SearchForm2
from home.models import Setting , ContactFormu , ContactFormMessage , UserProfile , FAQ

from house.models import House , Category , Images , Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = House.objects.order_by('?').all()[:4]
    category = Category.objects.all()
    yeniEklenenler = House.objects.all().order_by('-id')[:4]

    context = {'setting': setting ,
               'category': category ,
               'page': 'home' ,
               'yeniEklenenler': yeniEklenenler ,
               'sliderdata': sliderdata ,

               }

    return render(request , "index.html" , context)


def hakkimizda(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'category':category,
        'setting': setting ,
        'page': 'hakkimizda'}
    return render(request , "hakkimizda.html" , context)


def ilanlar(request):
    category = Category.objects.all()
    houses = House.objects.all()
    setting = Setting.objects.get(pk=1)

    context = {
        'setting': setting ,
        'category': category ,
               'houses': houses}
    return render(request , "ilanlar.html" , context)


def category_ilanlar(request , id , slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    houses = House.objects.filter(category_id=id)
    if not houses:
        houses = House.objects.filter(category__parent_id__exact=id)

    context = {'houses': houses ,
               'category': category ,
               'categorydata': categorydata ,
               }
    return render(request , "ilanlar.html" , context)


def iletisim(request):
    form = ContactFormu()
    category = Category.objects.all()

    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # model ile baglantı kurma
            data.name = form.cleaned_data['name']  # formdan bilgi alma
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # veritabanına kaydetme
            messages.success(request , 'Mesajınız baaşarı ile gönderilmiştir.Teşekkür ederiz')
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'category': category ,
    'setting': setting , 'form': form}
    return render(request , 'iletisim.html' , context)


def UrunSayfasi(request , id , slug):
    category = Category.objects.all()
    house = House.objects.get(pk=id)
    comments=Comment.objects.filter(house_id=id,status=True)
    images = Images.objects.filter(house_id=id)
    setting = Setting.objects.get(pk=1)
    is_favorite=False
    context = {'category': category ,
               'comments' :comments,
               'setting' :setting,
               'house': house ,
               'images': images ,
               }

    mesaj = "Ev" , id , "/" , slug
    return render(request , 'singleEvDetay.html' , context)


def house_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            cityid = form.cleaned_data['cityid']
            priceid = form.cleaned_data['priceid']
            if (catid == 0) & (priceid == 0) & (cityid == 0):
                print('1')

                print(cityid)
                houses = House.objects.filter(title__icontains=query)
            elif (cityid == "-") & (priceid == 0):
                print(' 2 ')
                houses = House.objects.filter(title__icontains=query , category_id=catid)
            elif (catid == 0) & (priceid == 0):
                print(' 3 ')
                houses = House.objects.filter(title__icontains=query , city__icontains=cityid)
            elif (cityid == "-") & (catid == 0):
                print(' 4 ')
                houses = House.objects.filter(title__icontains=query , price__lte=priceid)
            elif (catid == 0):
                print(' 5 ')
                houses = House.objects.filter(title__icontains=query , city__exact=cityid , price__lte=priceid)
            elif (cityid == "-"):
                print(' 6 ')
                houses = House.objects.filter(title__icontains=query , category_id=catid , price__lte=priceid)
            elif (priceid == 0):
                print(' 7 ')
                houses = House.objects.filter(title__icontains=query , city__exact=cityid , category_id=catid)

            print(houses)
            context = {'houses': houses ,

                       'category': category ,
                       }
            return render(request , 'ilanlar.html' , context)


def house_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term' , '')
        house = House.objects.filter(title__icontains=q)
        results = []
        for rs in house:
            house_json = {}
            house_json = rs.title
            results.append(house_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data , mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username=username , password=password)
        if user is not None:
            login(request , user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request , "Kullanıcı adı veya şifre yanlış!")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {
        'category': category ,
    }
    return render(request , 'login.html' , context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request , username=username , password=password)
            login(request , user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = 'images/users/user.png'
            data.save()
            return HttpResponseRedirect('/')
    form = SignUpForm()
    category = Category.objects.all()
    context = {
        'category': category ,
        'form': form ,
    }
    return render(request , 'signup.html' , context)







def filter(request):
    houses = House.objects.all()
    q1 = "title__icontains=query2"
    q2= False
    q3 = False
    q4 = False
    q5 = False
    q6= False
    q7 = False
    q8 = False
    q9 = False
    q10 = False
    q1 = False
    query2 = request.GET.get('query2')
    catid2 = request.GET.get('catid2')
    cityid2 = request.GET.get('cityid2')
    minbedid = request.GET.get('minbedid')
    districtid = request.GET.get('districtid')
    minbathid = request.GET.get('minbathid')
    minpriceid = request.GET.get('minpriceid')
    maxpriceid = request.GET.get('maxpriceid')
    minareaid = request.GET.get('minareaid')
    maxareaid = request.GET.get('maxareaid')
    print(query2)
    print(catid2)
    print(cityid2)
    print(minbedid)
    print(districtid)
    if is_valid_queryparam(query2):
        print("1")
        houses = House.objects.filter(title__icontains=query2)
        print(houses)
        girdi1 = True
    if is_valid_queryparam(catid2):
        print("2")
        if is_valid_queryparam(query2):
            houses = House.objects.filter(title__icontains=query2 , category_id=catid2)
        else:
            houses = House.objects.filter(category_id=catid2)

    if is_valid_queryparam(districtid):
        print("3")
        if is_valid_queryparam(query2):
            houses = House.objects.filter(title__icontains=query2 , district__icontains=districtid)
            if is_valid_queryparam(catid2):
                houses = House.objects.filter(title__icontains=query2 , category_id=catid2 ,district__icontains=districtid)
        else:
            if is_valid_queryparam(catid2):
                houses = House.objects.filter(category_id=catid2 , district__icontains=districtid)
            else:
                houses = House.objects.filter(district__icontains=districtid)

    if is_valid_queryparam(cityid2):
        print("4")
        if is_valid_queryparam(query2):
            houses = House.objects.filter(title__icontains=query2 , city__exact=cityid2)
            if is_valid_queryparam(catid2):
                houses = House.objects.filter(title__icontains=query2 , category_id=catid2 , city__exact=cityid2)
                if is_valid_queryparam(districtid):
                    houses = House.objects.filter(title__icontains=query2 , category_id=catid2 , city__exact=cityid2 ,
                                                  district__icontains=districtid)
            else:
                if is_valid_queryparam(districtid):
                    houses = House.objects.filter(title__icontains=query2 , city__exact=cityid2 ,
                                                  district__icontains=districtid)

        else:
            if is_valid_queryparam(catid2):
                houses = House.objects.filter(category_id=catid2 , city__exact=cityid2)
                if is_valid_queryparam(districtid):
                    houses = House.objects.filter(category_id=catid2 , city__exact=cityid2 ,
                                                  district__icontains=districtid)
            else:
                if is_valid_queryparam(districtid):
                    houses = House.objects.filter(city__exact=cityid2 , district__icontains=districtid)
                else:
                    houses = House.objects.filter(city__exact=cityid2)

    if is_valid_queryparam(minpriceid):
        print("5")
        if is_valid_queryparam(query2):
            houses = House.objects.filter(title__icontains=query2 , price__gte=minpriceid)
            if is_valid_queryparam(catid2):
                houses = House.objects.filter(title__icontains=query2 , category_id=catid2 , price__gte=minpriceid)
                if is_valid_queryparam(districtid):
                    houses = House.objects.filter(title__icontains=query2 , category_id=catid2 ,
                                                  price__gte=minpriceid , district__icontains=districtid)
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(title__icontains=query2 , category_id=catid2 ,
                                                      city__exact=cityid2 , district__icontains=districtid ,
                                                      price__gte=minpriceid)
                else:
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(title__icontains=query2 , category_id=catid2 ,
                                                      city__exact=cityid2 , price__gte=minpriceid)


            else:
                if is_valid_queryparam(districtid):
                    houses = House.objects.filter(title__icontains=query2 , price__gte=minpriceid ,
                                                  district__icontains=districtid)
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(title__icontains=query2 ,
                                                      city__exact=cityid2 , district__icontains=districtid ,
                                                      price__gt=minpriceid)
                else:
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(title__icontains=query2 ,
                                                      city__exact=cityid2 , price__gte=minpriceid)

        else:
            print('query')
            if is_valid_queryparam(catid2) | (catid2 != ""):
                houses = House.objects.filter(category_id=catid2 , price__gte=minpriceid)
                if is_valid_queryparam(districtid):
                    houses = House.objects.filter(category_id=catid2 , price__gte=minpriceid ,
                                                  district__icontains=districtid)
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(category_id=catid2 ,
                                                      city__exact=cityid2 , district__icontains=districtid ,
                                                      price__gte=minpriceid)
                else:

                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(category_id=catid2 ,
                                                      city__exact=cityid2 , price__gte=minpriceid)
            else:
                print('catid2')
                if is_valid_queryparam(districtid):
                    houses = House.objects.filter(price__gt=minpriceid ,
                                                  district__icontains=districtid)
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(
                            city__exact=cityid2 , district__icontains=districtid ,
                            price__gte=minpriceid)
                else:
                    print("district")
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(
                            city__exact=cityid2 , price__gte=minpriceid)
                    else:
                        print('come here')
                        houses = House.objects.filter(price__gte=minpriceid)

    if is_valid_queryparam(maxpriceid):
        print("6")
        if is_valid_queryparam(query2):
            print("buraya giriyor")
            houses = House.objects.filter(title__icontains=query2 , price__lte=maxpriceid)
            if is_valid_queryparam(catid2):
                houses = House.objects.filter(title__icontains=query2 , category_id=catid2 , price__lte=maxpriceid)
                if is_valid_queryparam(districtid):
                    houses = House.objects.filter(title__icontains=query2 , category_id=catid2 ,
                                                  price__lte=maxpriceid , district__icontains=districtid)
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(title__icontains=query2 , category_id=catid2 ,
                                                      city__exact=cityid2 , district__icontains=districtid ,
                                                      price__lte=maxpriceid)
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , category_id=catid2 ,
                                                          city__exact=cityid2 , district__icontains=districtid ,
                                                          price__lte=maxpriceid , price__gte=minpriceid)
                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , category_id=catid2 ,
                                                          district__icontains=districtid ,
                                                          price__lte=maxpriceid , price__gte=minpriceid)
                else:
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(title__icontains=query2 , category_id=catid2 ,
                                                      city__exact=cityid2 , price__gte=minpriceid)
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , category_id=catid2 ,
                                                          city__exact=cityid2 ,
                                                          price__lte=maxpriceid , price__gte=minpriceid)
                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , category_id=catid2 ,
                                                          price__lte=maxpriceid , price__gte=minpriceid)


            else:
                if is_valid_queryparam(districtid):
                    houses = House.objects.filter(title__icontains=query2 ,
                                                  price__lte=maxpriceid , district__icontains=districtid)
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(title__icontains=query2 ,
                                                      city__exact=cityid2 , district__icontains=districtid ,
                                                      price__lte=maxpriceid)
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 ,
                                                          city__exact=cityid2 , district__icontains=districtid ,
                                                          price__lte=maxpriceid , price__gte=minpriceid)
                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 ,
                                                          district__icontains=districtid ,
                                                          price__lte=maxpriceid , price__gte=minpriceid)
                else:
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(title__icontains=query2 ,
                                                      city__exact=cityid2 , price__gte=minpriceid)
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 ,
                                                          city__exact=cityid2 ,
                                                          price__lte=maxpriceid , price__gte=minpriceid)
                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 ,
                                                          price__lte=maxpriceid , price__gte=minpriceid)

        else:
            print('query')
            if is_valid_queryparam(catid2):
                houses = House.objects.filter(category_id=catid2 , price__lte=maxpriceid)
                if is_valid_queryparam(districtid):
                    houses = House.objects.filter(category_id=catid2 ,
                                                  price__lte=maxpriceid , district__icontains=districtid)
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(category_id=catid2 ,
                                                      city__exact=cityid2 , district__icontains=districtid ,
                                                      price__lte=maxpriceid)
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(category_id=catid2 ,
                                                          city__exact=cityid2 , district__icontains=districtid ,
                                                          price__lte=maxpriceid , price__gte=minpriceid)
                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(category_id=catid2 ,
                                                          district__icontains=districtid ,
                                                          price__lte=maxpriceid , price__gte=minpriceid)
                else:
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(category_id=catid2 ,
                                                      city__exact=cityid2 , price__gte=minpriceid)
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(category_id=catid2 ,
                                                          city__exact=cityid2 ,
                                                          price__lte=maxpriceid , price__gte=minpriceid)
                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(category_id=catid2 ,
                                                          price__lte=maxpriceid , price__gte=minpriceid)

            else:
                print('catid2')
                if is_valid_queryparam(districtid):
                    houses = House.objects.filter(
                        price__lte=maxpriceid , district__icontains=districtid)
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(
                            city__exact=cityid2 , district__icontains=districtid ,
                            price__lte=maxpriceid)
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(
                                city__exact=cityid2 , district__icontains=districtid ,
                                price__lte=maxpriceid , price__gte=minpriceid)
                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(
                                district__icontains=districtid ,
                                price__lte=maxpriceid , price__gte=minpriceid)
                else:
                    print('district')
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(
                            city__exact=cityid2 , price__gte=minpriceid)
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(
                                city__exact=cityid2 ,
                                price__lte=maxpriceid , price__gte=minpriceid)
                    else:
                        print("city")
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(price__lte=maxpriceid , price__gte=minpriceid)
                        else:
                            print("buraya gel")
                            houses = House.objects.filter(price__lte=maxpriceid)

    if is_valid_queryparam(minareaid):
        print("minarearea")
        if is_valid_queryparam(query2):
            print("buraya giriyor")

            houses = House.objects.filter(title__icontains=query2, area__gte=minareaid)
            if is_valid_queryparam(catid2):
                houses = House.objects.filter(title__icontains=query2, area__gte=minareaid,category_id=catid2)
                if is_valid_queryparam(districtid):
                    houses = House.objects.filter(title__icontains=query2, area__gte=minareaid,category_id=catid2,district__icontains=districtid)
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid ,
                                                      category_id=catid2 , district__icontains=districtid,city__exact=cityid2)

                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid ,
                                                          category_id=catid2 , district__icontains=districtid ,
                                                          city__exact=cityid2,price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              city__exact=cityid2 ,price__gte=minpriceid, price__lte=maxpriceid)
                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              city__exact=cityid2 ,  price__lte=maxpriceid)
                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid ,
                                                          category_id=catid2 , district__icontains=districtid ,
                                                          price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              price__gte=minpriceid , price__lte=maxpriceid)
                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid ,
                                                              category_id=catid2 , district__icontains=districtid , price__lte=maxpriceid)
                else:
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid ,
                                                      category_id=catid2 ,
                                                      city__exact=cityid2)

                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid ,
                                                          category_id=catid2 , city__exact=cityid2 , price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid ,
                                                              category_id=catid2,city__exact=cityid2 , price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid ,
                                                              category_id=catid2,city__exact=cityid2 , price__lte=maxpriceid)
                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid ,
                                                          category_id=catid2,price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid ,
                                                              category_id=catid2,price__gte=minpriceid , price__lte=maxpriceid)
                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid ,
                                                              category_id=catid2 ,price__lte=maxpriceid)


            else:
                if is_valid_queryparam(districtid):
                    houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid ,
                                                  district__icontains=districtid)
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid, district__icontains=districtid ,
                                                      city__exact=cityid2)

                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid, district__icontains=districtid ,
                                                          city__exact=cityid2 , price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid, district__icontains=districtid ,
                                                              city__exact=cityid2 , price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid, district__icontains=districtid ,
                                                              city__exact=cityid2 , price__lte=maxpriceid)
                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid  , district__icontains=districtid ,
                                                          price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid, district__icontains=districtid ,
                                                              price__gte=minpriceid , price__lte=maxpriceid)
                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid,district__icontains=districtid ,
                                                              price__lte=maxpriceid)
                else:
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid ,
                                                      city__exact=cityid2)

                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid , city__exact=cityid2 ,
                                                          price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid , city__exact=cityid2 ,
                                                              price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid , city__exact=cityid2 ,
                                                              price__lte=maxpriceid)
                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid , price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid, price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__gte=minareaid , price__lte=maxpriceid)

        else:
            print("query")
            if is_valid_queryparam(catid2):
                houses = House.objects.filter(area__gte=minareaid , category_id=catid2)
                if is_valid_queryparam(districtid):
                    houses = House.objects.filter(area__gte=minareaid , category_id=catid2 ,
                                                  district__icontains=districtid)
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(area__gte=minareaid ,
                                                      category_id=catid2 , district__icontains=districtid ,
                                                      city__exact=cityid2)

                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(area__gte=minareaid ,
                                                          category_id=catid2 , district__icontains=districtid ,
                                                          city__exact=cityid2 , price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__gte=minareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              city__exact=cityid2 , price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__gte=minareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              city__exact=cityid2 , price__lte=maxpriceid)
                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(area__gte=minareaid ,
                                                          category_id=catid2 , district__icontains=districtid ,
                                                          price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__gte=minareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              price__gte=minpriceid , price__lte=maxpriceid)
                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__gte=minareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              price__lte=maxpriceid)
                else:
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(area__gte=minareaid ,
                                                      category_id=catid2 ,
                                                      city__exact=cityid2)

                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(area__gte=minareaid ,
                                                          category_id=catid2 , city__exact=cityid2 ,
                                                          price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__gte=minareaid ,
                                                              category_id=catid2 , city__exact=cityid2 ,
                                                              price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__gte=minareaid ,
                                                              category_id=catid2 , city__exact=cityid2 ,
                                                              price__lte=maxpriceid)
                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(area__gte=minareaid ,
                                                          category_id=catid2 , price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__gte=minareaid ,
                                                              category_id=catid2 , price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__gte=minareaid ,
                                                              category_id=catid2 , price__lte=maxpriceid)


            else:
                if is_valid_queryparam(districtid):
                    houses = House.objects.filter(area__gte=minareaid ,
                                                  district__icontains=districtid)
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(area__gte=minareaid ,
                                                      district__icontains=districtid ,
                                                      city__exact=cityid2)

                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(area__gte=minareaid ,
                                                          district__icontains=districtid ,
                                                          city__exact=cityid2 , price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__gte=minareaid ,
                                                              district__icontains=districtid ,
                                                              city__exact=cityid2 , price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__gte=minareaid ,
                                                              district__icontains=districtid ,
                                                              city__exact=cityid2 , price__lte=maxpriceid)
                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(area__gte=minareaid ,
                                                          district__icontains=districtid ,
                                                          price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__gte=minareaid ,
                                                              district__icontains=districtid ,
                                                              price__gte=minpriceid , price__lte=maxpriceid)
                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__gte=minareaid ,
                                                              district__icontains=districtid ,
                                                              price__lte=maxpriceid)
                else:
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(area__gte=minareaid ,
                                                      city__exact=cityid2)

                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(area__gte=minareaid ,
                                                          city__exact=cityid2 ,
                                                          price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__gte=minareaid ,
                                                              city__exact=cityid2 ,
                                                              price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__gte=minareaid ,
                                                              city__exact=cityid2 ,
                                                              price__lte=maxpriceid)
                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(area__gte=minareaid ,
                                                          price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__gte=minareaid ,
                                                              price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__gte=minareaid ,
                                                              price__lte=maxpriceid)
    if is_valid_queryparam(maxareaid):
        print("max")
        if is_valid_queryparam(query2):
            houses= House.objects.filter(title__icontains=query2, area__lte=maxareaid)
            if is_valid_queryparam(catid2):
                houses= House.objects.filter(title__icontains=query2, area__lte=maxareaid,category_id=catid2)
                if is_valid_queryparam(districtid):
                    houses= House.objects.filter(title__icontains=query2, area__lte=maxareaid,category_id=catid2,district__icontains=districtid)
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                      category_id=catid2 , district__icontains=districtid,city__exact=cityid2)

                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                          category_id=catid2 , district__icontains=districtid ,
                                                          city__exact=cityid2,price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              city__exact=cityid2 , price__gte=minpriceid,price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__gte=minpriceid ,
                                                                  price__lte=maxpriceid,area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__gte=minpriceid , area__gte=minareaid)


                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              city__exact=cityid2 ,price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  city__exact=cityid2 ,price__lte=maxpriceid , area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  city__exact=cityid2 ,area__gte=minareaid)

                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                          category_id=catid2 , district__icontains=districtid, price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                              category_id=catid2 , district__icontains=districtid, price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid , price__gte=minpriceid ,
                                                                  price__lte=maxpriceid , area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid , price__gte=minpriceid ,
                                                                  area__gte=minareaid)


                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                              category_id=catid2 , district__icontains=districtid , price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid , price__lte=maxpriceid ,
                                                                  area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid , area__gte=minareaid)
                else:
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                      category_id=catid2 , district__icontains=districtid ,
                                                      city__exact=cityid2)

                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                          category_id=catid2 , district__icontains=districtid ,
                                                          city__exact=cityid2 , price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              city__exact=cityid2 , price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__gte=minpriceid ,
                                                                  price__lte=maxpriceid , area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__gte=minpriceid ,
                                                                  area__gte=minareaid)


                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              city__exact=cityid2 , price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__lte=maxpriceid ,
                                                                  area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  city__exact=cityid2 , area__gte=minareaid)

                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                          category_id=catid2 , district__icontains=districtid ,
                                                          price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  price__gte=minpriceid ,
                                                                  price__lte=maxpriceid , area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  price__gte=minpriceid ,
                                                                  area__gte=minareaid)


                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  price__lte=maxpriceid ,
                                                                  area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  area__gte=minareaid)
            else:
                if is_valid_queryparam(districtid):
                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid,district__icontains=districtid)
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,district__icontains=districtid ,
                                                      city__exact=cityid2)

                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,district__icontains=districtid ,
                                                          city__exact=cityid2 , price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid , district__icontains=districtid ,
                                                              city__exact=cityid2 , price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid, district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__gte=minpriceid ,
                                                                  price__lte=maxpriceid , area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid, district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__gte=minpriceid ,
                                                                  area__gte=minareaid)


                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid , district__icontains=districtid ,
                                                              city__exact=cityid2 , price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid, district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__lte=maxpriceid ,
                                                                  area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid, district__icontains=districtid ,
                                                                  city__exact=cityid2 , area__gte=minareaid)

                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid , district__icontains=districtid ,
                                                          price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid, district__icontains=districtid ,
                                                              price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid , district__icontains=districtid ,
                                                                  price__gte=minpriceid ,
                                                                  price__lte=maxpriceid , area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid,district__icontains=districtid ,
                                                                  price__gte=minpriceid ,
                                                                  area__gte=minareaid)


                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,district__icontains=districtid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid , district__icontains=districtid ,
                                                                  price__lte=maxpriceid ,
                                                                  area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid , district__icontains=districtid ,
                                                                  area__gte=minareaid)
                else:
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid , district__icontains=districtid ,
                                                      city__exact=cityid2)

                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid , district__icontains=districtid ,
                                                          city__exact=cityid2 , price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid, district__icontains=districtid ,
                                                              city__exact=cityid2 , price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid , district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__gte=minpriceid ,
                                                                  price__lte=maxpriceid , area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__gte=minpriceid ,
                                                                  area__gte=minareaid)


                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid ,district__icontains=districtid ,
                                                              city__exact=cityid2 , price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid, district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__lte=maxpriceid ,
                                                                  area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid , district__icontains=districtid ,
                                                                  city__exact=cityid2 , area__gte=minareaid)

                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid , district__icontains=districtid ,
                                                          price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid, district__icontains=districtid ,
                                                              price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid, district__icontains=districtid ,
                                                                  price__gte=minpriceid ,
                                                                  price__lte=maxpriceid , area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid , district__icontains=districtid ,
                                                                  price__gte=minpriceid ,
                                                                  area__gte=minareaid)


                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid , district__icontains=districtid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid, district__icontains=districtid ,
                                                                  price__lte=maxpriceid ,
                                                                  area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(title__icontains=query2 , area__lte=maxareaid , district__icontains=districtid ,
                                                                  area__gte=minareaid)

        else:
            print("query")
            if is_valid_queryparam(catid2):
                houses = House.objects.filter(area__lte=maxareaid , category_id=catid2)
                if is_valid_queryparam(districtid):
                    houses = House.objects.filter(area__lte=maxareaid , category_id=catid2 ,
                                                  district__icontains=districtid)
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(area__lte=maxareaid ,
                                                      category_id=catid2 , district__icontains=districtid ,
                                                      city__exact=cityid2)

                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(area__lte=maxareaid ,
                                                          category_id=catid2 , district__icontains=districtid ,
                                                          city__exact=cityid2 , price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__lte=maxareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              city__exact=cityid2 , price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__gte=minpriceid ,
                                                                  price__lte=maxpriceid , area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__gte=minpriceid ,
                                                                  area__gte=minareaid)


                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__lte=maxareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              city__exact=cityid2 , price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__lte=maxpriceid ,
                                                                  area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  city__exact=cityid2 , area__gte=minareaid)

                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(area__lte=maxareaid ,
                                                          category_id=catid2 , district__icontains=districtid ,
                                                          price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__lte=maxareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  price__gte=minpriceid ,
                                                                  price__lte=maxpriceid , area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  price__gte=minpriceid ,
                                                                  area__gte=minareaid)


                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__lte=maxareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  price__lte=maxpriceid ,
                                                                  area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  area__gte=minareaid)
                else:
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(area__lte=maxareaid ,
                                                      category_id=catid2 , district__icontains=districtid ,
                                                      city__exact=cityid2)

                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(area__lte=maxareaid ,
                                                          category_id=catid2 , district__icontains=districtid ,
                                                          city__exact=cityid2 , price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__lte=maxareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              city__exact=cityid2 , price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__gte=minpriceid ,
                                                                  price__lte=maxpriceid , area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__gte=minpriceid ,
                                                                  area__gte=minareaid)


                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__lte=maxareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              city__exact=cityid2 , price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__lte=maxpriceid ,
                                                                  area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  city__exact=cityid2 , area__gte=minareaid)

                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(area__lte=maxareaid ,
                                                          category_id=catid2 , district__icontains=districtid ,
                                                          price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__lte=maxareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  price__gte=minpriceid ,
                                                                  price__lte=maxpriceid , area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  price__gte=minpriceid ,
                                                                  area__gte=minareaid)


                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__lte=maxareaid ,
                                                              category_id=catid2 , district__icontains=districtid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  price__lte=maxpriceid ,
                                                                  area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  category_id=catid2 , district__icontains=districtid ,
                                                                  area__gte=minareaid)
            else:
                if is_valid_queryparam(districtid):
                    houses = House.objects.filter(area__lte=maxareaid ,
                                                  district__icontains=districtid)
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(area__lte=maxareaid ,
                                                      district__icontains=districtid ,
                                                      city__exact=cityid2)

                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(area__lte=maxareaid ,
                                                          district__icontains=districtid ,
                                                          city__exact=cityid2 , price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__lte=maxareaid ,
                                                              district__icontains=districtid ,
                                                              city__exact=cityid2 , price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__gte=minpriceid ,
                                                                  price__lte=maxpriceid , area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__gte=minpriceid ,
                                                                  area__gte=minareaid)


                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__lte=maxareaid ,
                                                              district__icontains=districtid ,
                                                              city__exact=cityid2 , price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__lte=maxpriceid ,
                                                                  area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  district__icontains=districtid ,
                                                                  city__exact=cityid2 , area__gte=minareaid)

                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(area__lte=maxareaid ,
                                                          district__icontains=districtid ,
                                                          price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__lte=maxareaid ,
                                                              district__icontains=districtid ,
                                                              price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  district__icontains=districtid ,
                                                                  price__gte=minpriceid ,
                                                                  price__lte=maxpriceid , area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  district__icontains=districtid ,
                                                                  price__gte=minpriceid ,
                                                                  area__gte=minareaid)


                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter( area__lte=maxareaid ,
                                                              district__icontains=districtid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  district__icontains=districtid ,
                                                                  price__lte=maxpriceid ,
                                                                  area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  district__icontains=districtid ,
                                                                  area__gte=minareaid)
                else:
                    if is_valid_queryparam(cityid2):
                        houses = House.objects.filter(area__lte=maxareaid ,
                                                      district__icontains=districtid ,
                                                      city__exact=cityid2)

                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(area__lte=maxareaid ,
                                                          district__icontains=districtid ,
                                                          city__exact=cityid2 , price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__lte=maxareaid ,
                                                              district__icontains=districtid ,
                                                              city__exact=cityid2 , price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__gte=minpriceid ,
                                                                  price__lte=maxpriceid , area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__gte=minpriceid ,
                                                                  area__gte=minareaid)


                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__lte=maxareaid ,
                                                              district__icontains=districtid ,
                                                              city__exact=cityid2 , price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  district__icontains=districtid ,
                                                                  city__exact=cityid2 , price__lte=maxpriceid ,
                                                                  area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  district__icontains=districtid ,
                                                                  city__exact=cityid2 , area__gte=minareaid)

                    else:
                        if is_valid_queryparam(minpriceid):
                            houses = House.objects.filter(area__lte=maxareaid ,
                                                          district__icontains=districtid ,
                                                          price__gte=minpriceid)
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__lte=maxareaid ,
                                                              district__icontains=districtid ,
                                                              price__gte=minpriceid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  district__icontains=districtid ,
                                                                  price__gte=minpriceid ,
                                                                  price__lte=maxpriceid , area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  district__icontains=districtid ,
                                                                  price__gte=minpriceid ,
                                                                  area__gte=minareaid)


                        else:
                            if is_valid_queryparam(maxpriceid):
                                houses = House.objects.filter(area__lte=maxareaid ,
                                                              district__icontains=districtid ,
                                                              price__lte=maxpriceid)
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  district__icontains=districtid ,
                                                                  price__lte=maxpriceid ,
                                                                  area__gte=minareaid)
                            else:
                                if is_valid_queryparam(minareaid):
                                    houses = House.objects.filter(area__lte=maxareaid ,
                                                                  district__icontains=districtid ,
                                                                  area__gte=minareaid)

    print(houses)

    return houses


def is_valid_queryparam(param):
    return param != '' and param is not None


def infinite_filter(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    return House.objects.all()[int(offset): int(offset) + int(limit)]


def is_there_more_data(request):
    offset = request.GET.get('offset')
    if int(offset) > House.objects.all().count():
        return False
    return True


def house_search2(request):
    houses = filter(request)
    print(houses)
    category = Category.objects.all()
    context = {
        'houses': houses ,
        'category': category
    }
    return render(request , "ilanlar.html" , context)

def faq(request):
    setting = Setting.objects.get(pk=1)

    category= Category.objects.all()
    faq=FAQ.objects.all().order_by('-ordernumber')
    context={
        'setting' : setting,
        'category':category,
        'faq': faq,
    }
    return render(request,'faq.html',context)