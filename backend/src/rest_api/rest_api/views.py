from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.template.loader import get_template

def home_page(request):
    my_title = "ArcadiaGaming"
    return render(request, "home.html", {"title" : my_title})