from django.urls import path
from . import views
from .views import homePageView, houseHoldPage, supplierPage, adminPage, indexPage, loginPage

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', homePageView, name='home'),
    path("household/<int:houseHoldId>/", houseHoldPage, name='household'),
    path('supplier', supplierPage, name='supplier'),
    path('administration', adminPage, name='admin'),
    path('index', indexPage, name='index')
]
