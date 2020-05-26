
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import SlugField
from django.http import HttpResponse , request , HttpResponseRedirect
from django.shortcuts import render , redirect

# Create your views here.
from home.models import UserProfile,Setting
from house.models import Category , House , Comment , HouseImageForm , CImages , Images
from user.forms import UserUpdateForm , ProfileUpdateForm
from content.models import Menu , HouseForm
from django.shortcuts import get_object_or_404


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
            messages.success(request , 'Hesabınız Güncellendi.')
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
            messages.success(request , 'Şifreniz Başarı ile değiştirildi !')
            return HttpResponseRedirect('/user')
        else:
            messages.warning(request , 'Please correct the error below !')
            return HttpResponseRedirect('/user/password')
    else:
        category=Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request , 'change_password.html' , {'form': form,'category':category})


def comments(request):
    category=Category.objects.all()
    current_user=request.user
    comments=Comment.objects.filter(user_id=current_user.id)
    context={
        'category':category,
        'comments':comments,
    }
    return render(request,'user_comments.html',context)

@login_required(login_url='/login')
def deletecomment(request,id):
    current_user=request.user
    Comment.objects.filter(id=id,user_id=current_user).delete()
    messages.success(request , 'Yorum başarıyla silindi !')
    return HttpResponseRedirect('/user/comments')


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
        setting = Setting.objects.get(pk=1)
        context={
            'setting': setting,
            'category': category,
            'form':form,
        }
    return render(request,'user_addhouse.html',context)


@login_required(login_url='/login')
def houseedit(request,id):
    house= House.objects.get(id=id)
    if request.method=="POST":
        form= HouseForm(request.POST,request.FILES,instance=house)
        if form.is_valid():
            form.save()
            messages.success(request,'Ev Güncellendi')
            return HttpResponseRedirect('/user/myhouses')
        else:
            messages.warning(request,'Ev Form Hatasi : '+str(form.errors))
            return HttpResponseRedirect('/user/houseedit/'+str(id))
    else:
        category = Category.objects.all()
        form=HouseForm(instance=house)
        context={
            'house' : house,
            'form' : form,
            'category' : category,

        }
    return render(request,'user_addhouse.html',context)
@login_required(login_url='/login')
def housedelete(request,id):
    current_user=request.user
    House.objects.filter(id=id,userOwner_id=current_user).delete()
    messages.success(request,"İlan Silindi!")
    return HttpResponseRedirect('/user/myhouses')
@login_required(login_url='/login')
def myhouses(requset):
    category=Category.objects.all()
    menu = Menu.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user=requset.user
    myhouses=House.objects.filter(userOwner_id=current_user.id)

    context = {
        'setting': setting,
        'category':category,
        'menu':menu,
        'myhouses':myhouses,
    }
    return render(requset,'user_myhouses.html',context)

def houseaddimage(request,id):

    if request.method=='POST':
        lasturl=request.META.get('HTTP_REFERER')
        form = HouseImageForm(request.POST,request.FILES)
        if form.is_valid():
            data=Images()
            data.title=form.cleaned_data['title']
            data.house_id=id
            data.image=form.cleaned_data['image']
            data.save()
            messages.success(request,'Fotograf basari ile yuklendi')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request,'Form Error :'+str(form.errors))
            return HttpResponseRedirect(lasturl)
    else:
        house=House.objects.get(id=id)
        images=Images.objects.filter(house_id=id)
        form=HouseImageForm()
        context = {
            'house': house,
            'images' : images,
            'form' : form,
        }
        return render(request , 'house_fotolar.html' , context)
@login_required(login_url='/login')
def fotodelete(request,id1,id2):
    lasturl = request.META.get('HTTP_REFERER')
    current_user=request.user
    Images.objects.filter(id=id1,house_id=id2).delete()
    messages.success(request,"İlan Silindi!")
    return HttpResponseRedirect(lasturl)