from django.urls import path

from .views import homePageView, houseHoldPage, supplierPage, adminPage

urlpatterns = [
    path('', homePageView, name='home'),
    path("household/<int:houseHoldId>/", houseHoldPage, name='household'),
    path('supplier', supplierPage, name='supplier'),
    path('administration', adminPage, name='admin')
]