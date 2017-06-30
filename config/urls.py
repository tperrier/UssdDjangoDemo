"""djangoUSSD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

import UssdHttp.simulator.views as sim
from UssdHttp.drivers.django_driver import session_list_view
import UssdDemo.views as demo

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', sim.NiafikraView.as_view()),
    url(r'^ussd_web/?$',demo.UssdDriver.as_view(transport='Niafikra')),
    url(r'^ussd/?$',demo.UssdDriver.as_view(transport='Niafikra')),
    url(r'^session/?$',session_list_view),
]
