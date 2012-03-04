from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from google.appengine.ext import db
from bootstrap.forms import BootstrapModelForm, Fieldset
from django.template import RequestContext
from django.conf import settings
from django.utils.importlib import import_module
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import gdata.auth
import gdata.gauth
import gdata.docs.data
import gdata.docs.client
import gdata.docs.service
from models import *

from google_oauth.views import oauth_start, get_client, clear_google_oauth_session, oauth_get_access_token
from google_oauth.views import GOOGLE_OAUTH_REQ_TOKEN, GOOGLE_OAUTH_TOKEN

from app.models import *
import os, sys, datetime, copy, logging, settings, json

STEP2_URI = 'https://beta.essaysafe.org/oauth2callback'

# Change everything in this class! Makes things pretty fast and easy
# so the basic info about the site is ubiquitous. 

CLIENT_ID = '1075895061839-air2l59at4t8gsng9ml8a3j0qspfp8i8.apps.googleusercontent.com'
CLIENT_SECRET = '6savVHl6blxgIwodzBRKXPMc'

class ExamForm(BootstrapModelForm):
  class Meta:
    model = Exam
    exclude = ('professor',)

def make(request):
  """Test callback view"""
  if request.method == 'POST':
    logging.info("in post")
    return info_submit(request)
  if request.session.get(GOOGLE_OAUTH_TOKEN, False):
    client = get_client(
          request.session[GOOGLE_OAUTH_TOKEN].token,
          request.session[GOOGLE_OAUTH_TOKEN].token_secret,
      )
    form = ExamForm()
    ##feed = client.GetDocList(uri='/feeds/default/private/full/-/document') 
    ##doclist = map (lambda entry: Doc(doc_name=entry.title.text.encode('UTF-8'), resource_id=entry.resource_id.text), feed.entry)
    context = {
      'form': form
    }
    return  render_to_response('make.html', RequestContext(request, context))
  elif request.session.get(GOOGLE_OAUTH_REQ_TOKEN, False):
    oauth_get_access_token(request)
    return HttpResponseRedirect("http://" + request.get_host() + request.path)
  else:
    return oauth_start(request)

def info_submit(request):
  if request.method == 'POST':
    post = request.POST
    try:
      client = get_client(
          request.session[GOOGLE_OAUTH_TOKEN].token,
          request.session[GOOGLE_OAUTH_TOKEN].token_secret,
      )
      logging.warning(post.get('start_date'))
      logging.warning(post.get('start_time'))
      logging.warning(post.get('end_date'))
      logging.warning(post.get('end_time'))
      logging.warning(post.get('exam_name'))
      date_format = '%m/%d%/%Y'
      time_format = '%I:%M%p'
      datetime_format = date_format+'-'+time_format
      start = post.get('start_date')+'-'+post.get('start_time')
      start_datetime = start_datetime = datetime.datetime(
              int(start[6:10]),
              int(start[0:2]),
              int(start[3:5]),
              int(start[11:13]),
              int(start[14:16])
              )
      logging.warning(start_datetime)
      end = post.get('end_date')+'-'+post.get('end_time')
      end_datetime = end_datetime = datetime.datetime(
              int(end[6:10]),
              int(end[0:2]),
              int(end[3:5]),
              int(end[11:13]),
              int(end[14:16])
              )
      prof_name = 'Random Prof'
      exam_name = post.get('exam_name')
      exam = Exam()
      if prof_name != 'Random Prof':
        exam.professor = Professor.objects.get(name=prof_name)
      exam.exam_name = exam_name
      logging.warning('done the exam name: '+exam_name)
      exam.start_time = start_datetime
      exam.end_time = end_datetime
      new_doc = create_doc(client, prof_name, exam_name)
      logging.warning('done the times')
      exam.resource_id = new_doc.resource_id.text
      exam.save()
      logging.warning('saved')
      new_doc = create_doc(client, prof_name, exam_name)
      logging.warning('created'+ str(new_doc.resource_id.text))
      logging.warning('created'+ str(new_doc.resource_id.text).split(':')[1])
      reply = {'success': True,
             'form_valid': True,
             'new_doc': str(new_doc.resource_id.text).split(':')[1]}
    except: 
      reply = {'success': True,
             'form_valid': False,
             'error_message': 'shit be fucked up'}
    return render_to_response('make.html',reply)
    
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

def create_doc(client, prof_name, exam_name): 
  """
  Create New Google Docs.
  """
  doc_name = prof_name + ' ' + exam_name
  try:
    folder = client.GetDocList(uri='/feeds/default/private/full/-/folder?title='+exam_name)[0]
  except:
    folder = client.Create(gdata.docs.data.FOLDER_LABEL, exam_name)
  new_doc = client.Create(gdata.docs.data.DOCUMENT_LABEL, doc_name, folder.resource_id.text)

  return new_doc

def CreateResourceInCollection(client, prof_name, exam_name):
  """Create a collection, then create a document in it."""
  col = gdata.docs.data.Resource(type='folder', title=exam_name)
  col = client.CreateResource(col)
  logging.warning('Created collection:', col.title.text, col.resource_id.text)
  doc = gdata.docs.data.Resource(type='document', title=exam_name+' prompt')
  doc = client.CreateResource(doc, collection=col)
  logging.warning('Created:', doc.title.text, doc.resource_id.text)
  return doc.resource_id.text