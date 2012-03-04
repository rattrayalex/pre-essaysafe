from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from google.appengine.ext import db

from django.conf import settings
from django.utils.importlib import import_module
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import gdata.auth
import gdata.gauth
import gdata.docs.data
import gdata.docs.client
import gdata.docs.service

from google_oauth.views import oauth_start, get_client, clear_google_oauth_session, oauth_get_access_token
from google_oauth.views import GOOGLE_OAUTH_REQ_TOKEN, GOOGLE_OAUTH_TOKEN

from app.models import *
import os, sys, datetime, copy, logging, settings

STEP2_URI = 'https://beta.essaysafe.org/oauth2callback'

# Change everything in this class! Makes things pretty fast and easy
# so the basic info about the site is ubiquitous. 

CLIENT_ID = '1075895061839-air2l59at4t8gsng9ml8a3j0qspfp8i8.apps.googleusercontent.com'
CLIENT_SECRET = '6savVHl6blxgIwodzBRKXPMc'

def make(request):
  """Test callback view"""
  if request.session.get(GOOGLE_OAUTH_TOKEN, False):
    client = get_client(
          request.session[GOOGLE_OAUTH_TOKEN].token,
          request.session[GOOGLE_OAUTH_TOKEN].token_secret,
      )
    logging.warning(client)
    feed = client.GetDocList(uri='/feeds/default/private/full/-/document')
    
    doclist = map (lambda entry: Doc(doc_name=entry.title.text.encode('UTF-8'), resource_id=entry.resource_id.text), feed.entry)
    return  render_to_response('make.html', {
      'doclist': doclist,
      })
  elif request.session.get(GOOGLE_OAUTH_REQ_TOKEN, False):
    oauth_get_access_token(request)
    return HttpResponseRedirect("http://" + request.get_host() + request.path)
  else:
    return oauth_start(request)


def index(request):
  context = {
    }
  return render_to_response('index.html', context)

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

def create_docs(request, exam_name, student_name): 
  """
  Create New Google Docs.
  """
  client = CreateClient()
  doc_name = prof_name + '_' + exam_name
  try:
    new_doc = client.Create(gdata.docs.data.DOCUMENT_LABEL, doc_name, folder_or_id=exam_name)
  except:
    new_folder = client.Create(gdata.docs.data.FOLDER_LABEL, 'My Folder')
  
  
  return True

