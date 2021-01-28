"""OwDR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from donationApp.views import LandingPage, AddDonation, Login, Logout, Register, DonationSuccessView,\
    get_institutions, UserProfileView, UserProfileUpdateView, PasswordChangeView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', LandingPage.as_view(), name='index'),
    path('add_donation/', AddDonation.as_view(), name='add_donation'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile_update/', UserProfileUpdateView.as_view(), name='profile_update'),
    path('change_password/', PasswordChangeView.as_view(), name='change_password'),
    path('get_institutions/', get_institutions, name='get_institutions'),
    path('form_confirmation/', DonationSuccessView.as_view(), name='donation_success')
]
