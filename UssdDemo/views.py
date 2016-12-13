from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import UssdHttp
import ussd_demo

class UssdDriver(UssdHttp.drivers.DjangoDriver):

    start_app = ussd_demo.app
