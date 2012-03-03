from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from google.appengine.ext import db

from app.models import *

import os, sys, datetime, copy, logging, settings


# Change everything in this class! Makes things pretty fast and easy
# so the basic info about the site is ubiquitous. 

  
def index(request):
  context = {
      }
  return render_to_response('index.html', context)
