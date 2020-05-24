from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import SlugField
from django.http import HttpResponse , request , HttpResponseRedirect
from django.shortcuts import render , redirect

# Create your views here.
from home.models import UserProfile
from house.models import Category , House
from user.forms import UserUpdateForm , ProfileUpdateForm
from content.models import Menu , HouseForm


def index(request):
    category=Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)

    context = {'profile': profile,
                'category':category,
               }
    return render(request , 'user_profile.html' , context)


def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST , instance=request.user)
        profile_form = ProfileUpdateForm(request.POST , request.FILES , instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request , 'Your account has been updated')
            return redirect('/user')
    else:
        category = Category.objects.all()

        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category ,
            'user_form': user_form ,
            'profile_form': profile_form ,
        }
        return render(request , 'user_update.html' , context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user , request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request , user)
            messages.success(request , 'Your password was succesfully updated !')
            return redirect('change_password')
        else:
            messages.warning(request , 'Please correct the error below !')
            return HttpResponseRedirect('/user/password')
    else:
        form = PasswordChangeForm(request.user)
        return render(request , 'change_password.html' , {'form': form})


def comments(request):
    return HttpResponse('calisti')
@login_required(login_url='/login')
def addhouse(request):
    if request.method=='POST':
        form=HouseForm(request.POST,request.FILES)
        if form.is_valid():
            current_user=request.user
            data=House()
            data.userOwner_id=current_user.id
            data.title=form.cleaned_data['title']
            data.slug=form.cleaned_data['slug']
            data.description=form.cleaned_data['description']
            data.keywords=form.cleaned_data['keywords']
            data.category=form.cleaned_data['category']
            data.price=form.cleaned_data['price']
            data.buildTime=form.cleaned_data['buildTime']
            data.city=form.cleaned_data['city']
            data.district=form.cleaned_data['district']
            data.locationDetail=form.cleaned_data['locationDetail']
            data.area=form.cleaned_data['area']
            data.bedroom=form.cleaned_data['bedroom']
            data.bathroom=form.cleaned_data['bathroom']
            data.garage=form.cleaned_data['garage']
            data.detail=form.cleaned_data['detail']
            data.image=form.cleaned_data['image']
            data.status=False
            data.save()
            messages.success(request,"ilan başarıyla eklendi")
            return HttpResponseRedirect('/user/myhouses')
        else:
            messages.warning(request,'İlan Formu Hata verdi:'+str(form.errors))
            return HttpResponseRedirect('user/myhouses')
    else:
        category=Category.objects.all()
        form=HouseForm()
        context={
            'category': category,
            'form':form,
        }
        return render(request,'user_addhouse.html',context)

def houseedit(request):
    return HttpResponse("Hello")

def housedelete(request):
    return HttpResponse("Hello")

@login_required(login_url='/login')
def myhouses(requset):
    category=Category.objects.all()
    menu = Menu.objects.all()
    current_user=requset.user
    myhouses=House.objects.filter(userOwner_id=current_user.id)

    context = {
        'category':category,
        'menu':menu,
        'myhouses':myhouses,
    }
    return render(requset,'user_myhouses.html',context)
