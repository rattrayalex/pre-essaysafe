from django.shortcuts import get_object_or_404
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
from gdata.acl.data import AclScope, AclRole
from app.forms import LogInForm, SignUpForm
from StringIO import StringIO

try: from functools import wraps
except ImportError: from django.utils.functional import wraps # Python 2.4 fallback.

from models import *
from django.contrib import auth

from box import listFoldersIn, uploadFile, listFilesIn

from google_oauth.views import oauth_start, get_client, clear_google_oauth_session, oauth_get_access_token
from google_oauth.views import GOOGLE_OAUTH_REQ_TOKEN, GOOGLE_OAUTH_TOKEN

from app.models import *
import os, sys, datetime, copy, logging, settings, json

STEP2_URI = 'https://beta.essaysafe.org/oauth2callback'

# Change everything in this class! Makes things pretty fast and easy
# so the basic info about the site is ubiquitous. 

CLIENT_ID = '1075895061839-air2l59at4t8gsng9ml8a3j0qspfp8i8.apps.googleusercontent.com'
CLIENT_SECRET = '6savVHl6blxgIwodzBRKXPMc'


def oauth_required(view_func):
    """
    Decorator for views to ensure that the user is sending an OAuth signed request.
    """
    def _checklogin(request, *args, **kwargs):
      if request.session.get(GOOGLE_OAUTH_TOKEN, False):
        return view_func(request, *args, **kwargs)
      elif request.session.get(GOOGLE_OAUTH_REQ_TOKEN, False):
        oauth_get_access_token(request)
        return HttpResponseRedirect("http://" + request.get_host() + request.path)
      else:
        return oauth_start(request)
    return wraps(view_func)(_checklogin)

@oauth_required
def transfer(request, folder_name):
  client = get_client(
    request.session[GOOGLE_OAUTH_TOKEN].token,
    request.session[GOOGLE_OAUTH_TOKEN].token_secret,
    )
  #feed = client.GetDocList(uri='/feeds/default/private/full/-/folder?title'+folder_name+'&title-exact=true&max-results=5')
  feed = client.GetDocList(uri='/feeds/default/private/full/-/folder')
  if len(feed.entry) > 1:
    logging.warning("folder name is matching with multiple files")
  folder = feed.entry[0]
  feed = client.GetDocList(uri=folder.content.src)
  for doc in feed.entry:
    content = client.GetFileContent(uri=doc.content.src)
    uploadFile(content)
    #file_path = 'remote:http://localhost:8080/filehandler'
    #client.Export(doc, file_path)

class ExamForm(BootstrapModelForm):
  class Meta:
    model = Exam
    exclude = ('professor',)

@login_required
def make(request):
  """Test callback view"""
  message = ''
  if request.method == 'POST':
    exams = Exam.objects.filter(name=request.POST.get('exam_name'))
    if len(exams) == 0:
      return info_submit(request)
    else: 
      message = 'Sorry, there is already an exam named "'+request.POST.get('exam_name')+'". Please choose another name.' 
  if request.session.get(GOOGLE_OAUTH_TOKEN, False):
    client = get_client(
          request.session[GOOGLE_OAUTH_TOKEN].token,
          request.session[GOOGLE_OAUTH_TOKEN].token_secret,
      )
    form = ExamForm()
    ##feed = client.GetDocList(uri='/feeds/default/private/full/-/document') 
    ##doclist = map (lambda entry: Doc(doc_name=entry.title.text.encode('UTF-8'), resource_id=entry.resource_id.text), feed.entry)
    context = {
      'form': form,
      'message': message,
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
    if len(post.get('start_time')) == 6:
      start_time = '0'+post.get('start_time')
      logging.warning('thar be 6')
    else:
      end_time = post.get('end_time')
    logging.warning(start_time)
    if len(post.get('end_time')) == 6:
      end_time = '0'+post.get('end_time')
    else:
      start_time = post.get('start_time')
    logging.warning(end_time)
    datetime_format = date_format+'-'+time_format
    start = post.get('start_date')+'-'+start_time
    logging.warning(start)
    start_datetime = start_datetime = datetime.datetime(
            int(start[0:4]),
            int(start[5:7]),
            int(start[8:10]),
            int(start[11:13]),
            int(start[14:16])
            )
    logging.warning(start_datetime)
    end = post.get('end_date')+'-'+end_time
    end_datetime = end_datetime = datetime.datetime(
            int(end[0:4]),
            int(end[5:7]),
            int(end[8:10]),
            int(end[11:13]),
            int(end[14:16])
            )
    prof = Professor.objects.get(user=request.user)
    exam_name = post.get('exam_name')
    exam = Exam()
    exam.professor = prof
    exam.name = exam_name
    logging.warning('done the exam name: '+exam_name)
    exam.start_time = start_datetime
    exam.end_time = end_datetime
    new_doc, new_folder = create_doc(request, client, prof, exam_name)
    logging.warning('done the times')
    exam.resource_id = new_doc.resource_id.text
    exam.folder_id = new_folder.resource_id.text
    exam.save()
    logging.warning('saved')
    logging.warning('created'+ str(new_doc.resource_id.text))
    logging.warning('created'+ str(new_doc.resource_id.text).split(':')[1])
    reply = {'success': True,
           'form_valid': True,
           'exam': exam,
           'new_doc': str(new_doc.resource_id.text).split(':')[1]}
    return render_to_response('make.html',RequestContext(request,reply))
    
def index(request):
  context = {
    }
  return render_to_response('index.html', context)

def take(request, exam_name, student_name, student_email):
  if request.session.get(GOOGLE_OAUTH_TOKEN, False):
    client = get_client(
          request.session[GOOGLE_OAUTH_TOKEN].token,
          request.session[GOOGLE_OAUTH_TOKEN].token_secret,
      )
    
    exam = get_object_or_404(Exam, name=exam_name)
    prof = exam.professor
    p_client = get_client(prof.token, prof.token_secret)
    prompt_doc_id = str(exam.resource_id)
    prompt_doc = client.GetDoc(prompt_doc_id)
    doc_name = exam_name+' | '+student_name
    student_doc = client.Copy(prompt_doc, doc_name)
    folder = client.GetDoc(exam.folder_id)
    new_student_doc = client.Move(student_doc, folder)
    #scope = AclScope(client)
    #role = AclRole('writer')
    #acl_entry = gdata.docs.data.Acl(scope=scope, role=role)
    #new_acl = client.Post(acl_entry, new_student_doc.GetAclFeedLink().href)
    ##feed = client.GetDocList(uri='/feeds/default/private/full/-/document') 
    ##doclist = map (lambda entry: Doc(doc_name=entry.title.text.encode('UTF-8'), resource_id=entry.resource_id.text), feed.entry)
    context = {
      'doc': str(student_doc.resource_id.text).split(':')[1]
    }
    return  render_to_response('take.html', RequestContext(request, context))
  elif request.session.get(GOOGLE_OAUTH_REQ_TOKEN, False):
    oauth_get_access_token(request)
    return HttpResponseRedirect("http://" + request.get_host() + request.path)
  else:
    return oauth_start(request)

@login_required
# @oath_required
def dashboard(request):
  prof = Professor.objects.get(user=request.user)
  box_id = prof.box_id
  # (name, id)
  exams = listFoldersIn(box_id)
  exam_count = dict()
  ids = []
  # for e in exams:
    # exam_count[e] = len(listFilesIn(exams[e]))
  for e in exams:
    
  context = {
    'exams': exams, 
	'ids': 
	'count': len(exams),
	'box_id': box_id,
	'exam_count':exam_count
  }
  return render_to_response('dashboard.html', context)

def distribute(request, exam_id):
  exam = Exam.objects.get(id=exam_id)
  context = {
    'exam': exam
  }
  return render_to_response('distribute.html', context)
  
def about(request):
  context = {
    }
  return render_to_response('about.html', context)

def create_doc(request, client, prof, exam_name): 
  """
  Create New Google Docs.
  """
  doc_name = exam_name + ' | Prompt'
  main_folder_id = prof.folder_id
  try:
    main_folder = client.GetDoc(main_folder_id)
    first_item = [d for d in client.GetDocList(main_folder.content.src).entry][0]
  except:
    main_folder = client.Create(gdata.docs.data.FOLDER_LABEL, 'EssaySafe')
    prof.folder_id = main_folder.resource_id.text
    prof.save()
  try:
    folder = client.GetDocList(uri='/feeds/default/private/full/-/folder/?title='+exam_name+'&title-exact=true&max-results=1').entry[0]
  except:
    pre_folder = client.Create(gdata.docs.data.FOLDER_LABEL, exam_name)
    folder = client.Move(pre_folder, main_folder)
  logging.warning(folder)
  #folder = client.Create(gdata.docs.data.FOLDER_LABEL, exam_name)
  ##new_doc = client.Create(gdata.docs.data.DOCUMENT_LABEL, doc_name, folder.resource_id.text)
  template = client.GetDoc('document:1OB40c2l26fL6BdRim1cKuQhG0Kyt8X6brsAvlVMQ1sE')
  new_doc = client.Copy(template, doc_name)
  newer_doc = client.Move(new_doc, folder)
  ##txt = gdata.data.MediaSource(file_path="http://" + request.get_host()+'/media/welcome.txt', content_type="text")
  ##newer_doc = client.Update(new_doc, media_source=txt)
  ##new_doc = client.Upload('media/welcome.txt', doc_name, folder.resource_id.text, content_type="text")
  return newer_doc, folder

def index(request):
  context = {
    }
  return render_to_response('index.html', context)
  
def login(request): 
  if request.method == 'POST':
    form = LogInForm(None, request.POST)
    next = request.POST['next']
    if form.is_valid():
      form.clean()
      user = form.user_cache
      if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect(request.POST['next'])
      else:
        return render_to_response('login.html', {'form': form, 
          'user': form.user_cache,}, context_instance=RequestContext(request))
  else:
    form = LogInForm() 
    next = request.GET.get('next', '/dashboard/')
  context = {'form': form, 'user': request.user, 'next': next}
  return render_to_response('login.html', context, context_instance=RequestContext(request))

def logout(request):
  auth.logout(request)
  return HttpResponseRedirect('/')

@oauth_required
def signup(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    next = request.POST['next']
    if form.is_valid():
      prof = form.save()
      user = auth.authenticate(username=request.POST['email'], 
        password=request.POST['password'])
      client = get_client(
          request.session[GOOGLE_OAUTH_TOKEN].token,
          request.session[GOOGLE_OAUTH_TOKEN].token_secret,
      )
      main_folder = client.Create(gdata.docs.data.FOLDER_LABEL, 'EssaySafe')
      prof.folder_id = main_folder.resource_id.text
      prof.token = request.session[GOOGLE_OAUTH_TOKEN].token
      prof.token_secret = request.session[GOOGLE_OAUTH_TOKEN].token_secret
      prof.save()
      if user is not None:
        auth.login(request, user)
      return HttpResponseRedirect(next)
  else:
    taken = False
    form = SignUpForm()
    next = request.GET.get('next', '/')
  context = {'form':form, 'next': next,}
  return render_to_response('signup.html', context, context_instance=RequestContext(request))
