from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from pymongo import MongoClient


from django import forms
from django.db import models
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from django.template import loader

from pages.forms import CreateUserForm

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error
from math import sqrt

from matplotlib.pylab import rcParams

@login_required(login_url='login')
def homePageView(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render({}, request))

def getAllData():
    mongo_client = MongoClient(
        "mongodb+srv://rdmo:Rdmrdm65@iotsewardmo-nt3ui.mongodb.net/test?retryWrites=true&w=majority")
    return mongo_client.iot.data

def indexPage(request):
    user = User
    data = getAllData()
    print("hey :)")
    timestamps = []
    timestamps_unix = []
    mwhs = []
    for doc in data.find({"id":"1"}):
        timestamps.append(pd.to_datetime(doc['timestamp']/1000, unit='s', infer_datetime_format=True))
        mwhs.append(int(doc['mwh']))
        timestamps_unix.append(int(doc['timestamp']))

        #print('timestamp: ' + str(doc['timestamp']))
        #print('timestamp pd: ' + str(pd.to_datetime(doc['timestamp'], unit='ms')))
        #25-08-2012 02:00

    timestamps_sorted, mwhs_sorted = zip(*sorted(zip(timestamps, mwhs)))
    print('sorted timestamp type: ' + str(type(timestamps_sorted[0])))
    print(timestamps_sorted)
    print(timestamps)

    df_data = {'timestamps': timestamps_sorted, 'mwhs': mwhs_sorted}

    df = pd.DataFrame(
        {'timestamps': timestamps_sorted, 'mwhs': mwhs_sorted},
        columns=['mwhs', 'timestamps'], index=timestamps_sorted)
    df.index.freq = pd.infer_freq(timestamps_sorted)
    #df.index.freq = 'h'
    print(str(df.index.freq))

    #df = pd.DataFrame(df_data, columns=['timestamps', 'mwhs'], index=mwhs_sorted)
    #df.sort_values(by=['timestamps'])
    # Converting the index as date
    #df.index = df.index.to_pydatetime()

    print(df)
    bro(df)
    return render(request, 'index.html')


def bro(df):
    rcParams['figure.figsize'] = 20, 10

    #df = pd.read_csv('D:/WORK/international-airline-passengers.csv',
    # arse_dates=['Month'],
    # index_col='Day')

    #df.index = pd.to_datetime(df.index)
    print("1")
    train, test = df.iloc[:90, 0], df.iloc[90:140, 0]
    model = ExponentialSmoothing(train, seasonal='mul', seasonal_periods=12).fit()
    pred = model.predict(start=test.index[0], end=test.index[-1])
    #pred = model.forecast(12).plot(style='--', marker='o', color='red', legend=True)

    plt.plot(train.index, train, label='Train')
    plt.plot(test.index, test, label='Test')
    plt.plot(pred.index, pred, label='Holt-Winters')
    plt.legend(loc='best')
    plt.show()

    #model = ExponentialSmoothing(train, trend='add', seasonal='add', seasonal_periods=12, damped=True)
    print("2")
    #hw_model = model.fit(optimized=True, use_boxcox=False, remove_bias=False)
    print("3")
    #pred = hw_model.predict(start=test.index[0], end=test.index[-1])
    print("4")

    #plt.plot(train.index, train, label='Train',)
    #df.plot(x='timestamps', y='mwhs')
    #plt.plot(test.index, test, label='Test')
    #plt.plot(pred.index, pred, label='Holt-Winters')
    #plt.legend(loc='best')
    #plt.show()


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
        circle_switcher = {
            0: "c4105d0d-6e00-43ad-b80b-ee3ed462c50e",
            1: "068b1bd9-82c1-4b99-aaa0-238e1fa16605",
            2: "5e0be09d-0684-46ae-940a-7eaefcfa1818",
            3: "e5738408-0052-41a3-ab86-8e82babbabf5",
        }
        return HttpResponse(
            template.render({"houseHoldId": houseHoldId, "chartId": switcher.get(houseHoldId, "Invalid id"), "circle_chartId": circle_switcher.get(houseHoldId)}, request))

    else:
        return render(request, 'unauthorized.html')

@login_required(login_url='login')
def adminPage(request):
    template = loader.get_template('administration.html')
    return HttpResponse(template.render({}, request))

@login_required(login_url='login')
def supplierPage(request):
    template = loader.get_template('supplier.html')
    return HttpResponse(template.render({}, request))
