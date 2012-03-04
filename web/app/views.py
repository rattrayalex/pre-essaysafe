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


def CreateClient():
  """Create a Documents List Client."""
  client = gdata.docs.client.DocsClient(source=SampleConfig.APP_NAME)
  client.http_client.debug = SampleConfig.DEBUG
  # Authenticate the user with CLientLogin, OAuth, or AuthSub.
  try:
    gdata.sample_util.authorize_client(
        client,
        service=client.auth_service,
        source=client.source,
        scopes=client.auth_scopes
    )
  except gdata.client.BadAuthentication:
    exit('Invalid user credentials given.')
  except gdata.client.Error:
    exit('Login Error')
  return client

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

def make(request):
  client = CreateClient()
  feed = client.GetDocList(limit = 10)
  doclist = map (lambda entry: Doc(doc_name=entry.title.text.encode('UTF-8'), resource_id_text=entry.resource_id.text), feed)
  return  render_to_response('make.html', {
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

def create_docs(request, exam_name, student_name): 
  """
  Create Google Docs.
  """
  client = CreateClient()
  doc_name = prof_name + '_' + exam_name
  new_doc = client.Create(gdata.docs.data.DOCUMENT_LABEL, doc_name, folder_or_id=exam_name)
  return True
