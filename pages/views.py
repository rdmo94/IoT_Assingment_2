from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


from django import forms
from django.db import models
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from django.template import loader

from pages.forms import CreateUserForm

@login_required(login_url='login')
def homePageView(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render({}, request))


def indexPage(request):
    user = User
    return render(request, 'index.html')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'registration/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)

@login_required(login_url='login')
def houseHoldPage(request, houseHoldId):
    userbro = request.user
    usermter = request.user.meterID
    containsId = request.user.containsId(houseHoldId)

    if containsId:
        template = loader.get_template('household.html')
        switcher = {
            0: "d658801e-444d-4710-901d-992ba40bfeee",
            1: "c591e2ff-6fbc-4ea9-890a-4e556f737285",
            2: "22f5bf8d-7347-47c0-9db4-d47489d8995e",
            3: "de17fbcd-ad05-4b42-b3fb-6bcde5de676f",
        }
        return HttpResponse(
            template.render({"houseHoldId": houseHoldId, "chartId": switcher.get(houseHoldId, "Invalid id")}, request))

    else:
        return render(request, 'unauthorized.html')



def adminPage(request):
    template = loader.get_template('admin.html')
    return HttpResponse(template.render({}, request))


def supplierPage(request):
    template = loader.get_template('supplier.html')
    return HttpResponse(template.render({}, request))
