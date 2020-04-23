import switch as switch
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.template import loader

def homePageView(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render({}, request))


def houseHoldPage(request, houseHoldId):
    template = loader.get_template('household.html')
    switcher = {
        0: "d658801e-444d-4710-901d-992ba40bfeee",
        1: "c591e2ff-6fbc-4ea9-890a-4e556f737285",
        2: "22f5bf8d-7347-47c0-9db4-d47489d8995e",
        3: "de17fbcd-ad05-4b42-b3fb-6bcde5de676f",
    }
    return HttpResponse(template.render({"houseHoldId": houseHoldId, "chartId": switcher.get(houseHoldId, "Invalid id")}, request))

def adminPage(request):
    template = loader.get_template('admin.html')
    return HttpResponse(template.render({}, request))

def supplierPage(request):
    template = loader.get_template('supplier.html')
    return HttpResponse(template.render({}, request))