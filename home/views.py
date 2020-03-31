from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import context

from home.models import Setting


def index(request):
    setting= Setting.objects.get(pk=1)
    context={'setting':setting}
    return render(request, "index.html",context)


def properties(request):
    return render(request, "ilanlar.html", )


def iletisim(request):
    return render(request, "iletisim.html",)


def singleSayfa(request):
    return render(request, "singleEvDetay.html", )
