from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from google.appengine.ext import db

from django.conf import settings
from django.utils.importlib import import_module

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from oauth2client.django_orm import Storage
from oauth2client.client import OAuth2WebServerFlow
from apiclient.discovery import build

import gdata.docs.data
import gdata.docs.client

from app.models import *
import os, sys, datetime, copy, logging, settings, httplib2

STEP2_URI = 'https://www.essaysafe.com/oauth2callback'

# Change everything in this class! Makes things pretty fast and easy
# so the basic info about the site is ubiquitous. 

def warmup(request):
  """
  Provides default procedure for handling warmup requests on App Engine.
  Just add this view to your main urls.py.
  """
  for app in settings.INSTALLED_APPS:
    for name in ('urls', 'views', 'models'):
      try:
        import_module('%s.%s' % (app, name))
      except ImportError:
        pass
    content_type = 'text/plain; charset=%s' % settings.DEFAULT_CHARSET
    return HttpResponse('Warmup done', content_type=content_type)

def make(request):
  context = {
    }
  return render_to_response('make.html', context)

def take(request):
  context = {
    }
  return render_to_response('take.html', context)

def dashboard(request):
  context = {
    }
  return render_to_response('dashboard.html', context)

def about(request):
  context = {
    }
  return render_to_response('about.html', context)

@login_required
def index(request):
  storage = Storage(CredentialsModel, 'id', request.user, 'credential')
  credential = storage.get()
  if credential is None or credential.invalid == True:
    flow = OAuth2WebServerFlow(
      client_id='1099323164997.apps.googleusercontent.com',
      client_secret='68ZG8DjELFGQTZLIKur8wrTS',
      scope='https://www.googleapis.com/auth/plus.me',
      user_agent='plus-django-sample/1.0',
      )
    authorize_url = flow.step1_get_authorize_url(STEP2_URI)
    f = FlowModel(id=request.user, flow=flow)
    f.save()
    return HttpResponseRedirect(authorize_url)
  else:
    http = httplib2.Http()
    http = credential.authorize(http)
    service = build("essaysafe", "v1", http=http)
    
    feed = client.GetDocList(limit = 10)
    doclist = map (lambda entry: Doc(doc_name=entry.title.text.encode('UTF-8'), resource_id_text=entry.resource_id.text), feed)

    return  render_to_response('app/menu.html', {
        'doclist': doclist,
        })
  
@login_required
def auth_return(request):
  try:
    f = FlowModel.objects.get(id=request.user)
    credential = f.flow.step2_exchange(request.REQUEST)
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    f.delete()
    return HttpResponseRedirect("/")
  except FlowModel.DoesNotExist:
    pass

def create_docs(request, prof_name, exam_name, student_name): 
  """
  Create Google Docs.
  """
  doc_name = prof_name + '_' + exam_name
  new_doc = client.Create(gdata.docs.data.DOCUMENT_LABEL, doc_name, folder_or_id=exam_name)
  return True
