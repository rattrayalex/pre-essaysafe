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
from google.appengine.api import mail

import gdata.docs.service

import simplejson

import simplejson

try: from functools import wraps
except ImportError: from django.utils.functional import wraps # Python 2.4 fallback.

from models import *
from django.contrib import auth

from settings import ES_TOKEN, ES_TOKEN_SECRET, APP_NAME
from box import listFoldersIn, uploadFile, listFilesIn

from google_oauth.views import oauth_start, get_client, clear_google_oauth_session, oauth_get_access_token
from google_oauth.views import GOOGLE_OAUTH_REQ_TOKEN, GOOGLE_OAUTH_TOKEN

from app.models import *
import os, sys, datetime, copy, logging, settings, json

import gdata.docs.service

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
def transfer_file(request, essay_id):
  client = get_client(
    request.session[GOOGLE_OAUTH_TOKEN].token,
    request.session[GOOGLE_OAUTH_TOKEN].token_secret,
    )
  #feed = client.GetDocList(uri='/feeds/default/private/full/-/folder?title'+folder_name+'&title-exact=true&max-results=5')
  essay = Essay.objects.get(id=essay_id)
  doc = client.GetDoc(essay.resource_id)
  content = client.GetFileContent(uri=doc.content.src)
  email = essay.exam.box_email
  email_a_file(email, essay.exam.name+'_'+essay.student_name, content)
  return HttpResponseRedirect('/done')

@oauth_required
def transfer_exam(request, exam_name):
  client = get_client(
    request.session[GOOGLE_OAUTH_TOKEN].token,
    request.session[GOOGLE_OAUTH_TOKEN].token_secret,
    )
  #feed = client.GetDocList(uri='/feeds/default/private/full/-/folder?title'+folder_name+'&title-exact=true&max-results=5')
  #exam = Exam.objects.get(name=exam_name)
  feed = client.GetDocList(uri='/feeds/default/private/full/-/document')

  #if len(exam) > 1:
  #  logging.warning("exam name is matching with multiple exams")
  #essays = Essay.objects.select_related('exam')
  #for essay in essays:
  for doc in feed.entry:
    content = client.GetFileContent(uri=doc.content.src)
    email_a_file('upload.prof_pa.x9z8elbe7u@u.box.com', doc.title.text, content)
  
    return HttpResponseRedirect('/done')  

class ExamForm(BootstrapModelForm):
  class Meta:
    model = Exam
    exclude = ('professor',)

@login_required
def make(request):
  """Test callback view"""
  client = gdata.docs.service.DocsService()
  client.ClientLogin('essay.safe.hack@gmail.com', 'angelhack')
  documents_feed = client.GetDocumentListFeed()
  for document_entry in documents_feed.entry:
      logging.warning(document_entry.title.text)
  message = ''
  if request.method == 'POST':
    exams = Exam.objects.filter(name=request.POST.get('exam_name'))
    if len(exams) == 0:
      return info_submit(request)
    else: 
      message = 'Sorry, there is already an exam named "'+request.POST.get('exam_name')+'". Please choose another name.' 
  client = gdata.docs.client.DocsClient()
  auth_token = client.ClientLogin('essay.safe.hack@gmail.com','angelhack', APP_NAME)
  form = ExamForm()
  ##feed = client.GetDocList(uri='/feeds/default/private/full/-/document') 
  ##doclist = map (lambda entry: Doc(doc_name=entry.title.text.encode('UTF-8'), resource_id=entry.resource_id.text), feed.entry)
  context = {
    'form': form,
    'message': message,
  }
  return render_to_response('make.html', RequestContext(request, context))

def info_submit(request):
  if request.method == 'POST':
    post = request.POST
    client = gdata.docs.client.DocsClient()
    auth_token = client.ClientLogin('essay.safe.hack@gmail.com','angelhack', APP_NAME)
    date_format = '%m/%d%/%Y'
    time_format = '%I:%M%p'
    if len(post.get('start_time')) == 6:
      start_time = '0'+post.get('start_time')
    else:
      end_time = post.get('end_time')
    logging.warning(start_time)
    if len(post.get('end_time')) == 6:
      end_time = '0'+post.get('end_time')
    else:
      start_time = post.get('start_time')
    logging.warning(end_time)
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
    exam.box_fid = createSubFolder(prof.box_id, exam_name)
    element = getBox('toggle_folder_email', {'folder_id':folder_id, 'enable':'1'})
    exam.box_email = getText(element, 'upload_email')
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

def send_app_email(receiver, subject, body, attachments=None):
  logging.warning("in send_app_email")
  logging.warning(attachments)
  if attachments:
    logging.warning('there are attachments')
    mail.send_mail(sender='intouch.registrator@gmail.com',
                   to=receiver,
                   subject=subject,
                   body=body,
                   attachments=attachments)
  else:
    mail.send_mail(sender='intouch.registrator@gmail.com',
                   to=receiver,
                   subject=subject,
                   body=body)
  return "sent"

def email_a_file(add_email, filename, stream):
  logging.warning('in email_file')
  msg = "You have received a file from essaysafe.appspot.com"
  subject = 'New File from UploadToMail'
  attachments = [(filename, stream)]
  send_app_email((add_email,), subject, msg, attachments)
  logging.warning("sent"+str(attachments))
  return 1

def take(request, exam_name, student_name, student_email):
  client = gdata.docs.client.DocsClient()
  auth_token = client.ClientLogin('essay.safe.hack@gmail.com','angelhack', APP_NAME)
  exam = get_object_or_404(Exam, name=exam_name)
  prof = exam.professor
  prompt_doc_id = str(exam.resource_id)
  prompt_doc = client.GetDoc(prompt_doc_id)
  doc_name = exam_name+' | '+student_name
  student_doc = client.Copy(prompt_doc, doc_name)
  folder = client.GetDoc(exam.folder_id)
  new_student_doc = client.Move(student_doc, folder)
  scope = AclScope(value=student_email, type='user')
  role = AclRole(value='writer')
  acl_entry = gdata.docs.data.Acl(scope=scope, role=role)
  new_acl = client.Post(acl_entry, new_student_doc.GetAclFeedLink().href)
  context = {
    'doc': str(student_doc.resource_id.text).split(':')[1]
  }
  return render_to_response('take.html', RequestContext(request, context))
  
def dashboard(request):
  prof = Professor.objects.get(user=request.user)
  box_id = prof.box_id
  # (name, id)
  exams = listFoldersIn(box_id)
  exam_count = dict()
  ids = []
  for e in exams:
    exam_count[e] = [len(listFilesIn(exams[e])), exams[e]]
  context = {
    'exams': exams, 
	'ids': ids,
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

def getfiles(request):  
  if request.GET:
    f_id = request.GET['folder_id']
    logging.warning(str(f_id))
    files = listFilesIn(f_id)
    links = dict()
    for f in files:
      links[f] = url(str(files[f]))
    logging.info(links)
    return HttpResponse(simplejson.dumps(links), content_type='application/json')

def url(ID):
  return 'https://www.box.net/api/1.0/download/%s/%s' % ('8kf9roqysu8jmqskys9vg0hovkmyqtv3', ID)

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
  template = client.GetDoc('document:1OB40c2l26fL6BdRim1cKuQhG0Kyt8X6brsAvlVMQ1sE')
  new_doc = client.Copy(template, doc_name)
  newer_doc = client.Move(new_doc, folder)
  scope = AclScope(value=prof.email, type='user')
  role = AclRole(value='owner')
  acl_entry = gdata.docs.data.Acl(scope=scope, role=role)
  new_acl = client.Post(acl_entry, newer_doc.GetAclFeedLink().href)
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

def signup(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    next = request.POST['next']
    if form.is_valid():
      prof = form.save()
      user = auth.authenticate(username=request.POST['email'], 
        password=request.POST['password'])
      client = gdata.docs.client.DocsClient()
      auth_token = client.ClientLogin('essay.safe.hack@gmail.com','angelhack', APP_NAME)
      auth_token = client.ClientLogin('essay.safe.hack@gmail.com','angelhack', APP_NAME)
      main_folder = client.Create(gdata.docs.data.FOLDER_LABEL, 'EssaySafe | '+request.POST['email'])
      prof.folder_id = main_folder.resource_id.text
      #prof.token = request.session[GOOGLE_OAUTH_TOKEN].token
      #prof.token_secret = request.session[GOOGLE_OAUTH_TOKEN].token_secret
      #prof.auth_token = client.auth_token
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
