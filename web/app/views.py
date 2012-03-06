from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from bootstrap.forms import BootstrapModelForm, Fieldset
from django.template import RequestContext
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

try: from functools import wraps
except ImportError: from django.utils.functional import wraps # Python 2.4 fallback.
from models import *
from django.contrib import auth

from settings import APP_NAME, APP_PASS, APP_EMAIL
from box import listFoldersIn, uploadFile, listFilesIn, createSubFolder, getBox

from app.models import *
import os, sys, datetime, copy, logging, settings, json, simplejson

import gdata.docs.service

def docAuth():
  '''Authenticates with Google Docs'''
  client = gdata.docs.client.DocsClient()
  auth_token = client.ClientLogin(APP_EMAIL, APP_PASS, APP_NAME)
  return client

def submit_file(request, essay_id):
  '''Once a student is done, submits their essay. '''
  client = docAuth()
  
  essay = Essay.objects.get(id=essay_id) 
  doc = client.GetDoc(essay.resource_id)
  student_email = essay.student_email
  
  doc_code = doc.resource_id.text
  acl_entry = client.GetAclPermissions(doc_code).entry
  logging.warning(acl_entry)
  acl = acl_entry[1]
  logging.warning(acl)
  scope = acl.scope
  logging.warning(scope)
  acl.role.value = 'reader'
  new_acl = client.Update(acl, force=True)
  
  #content = client.GetFileContent(uri=doc.content.src)
  #email = essay.x_email
  #email_a_file(email, essay.exam.name+'_'+essay.student_name, content)
  return HttpResponseRedirect('../../../../done/%s/' % (essay_id))

class ExamForm(BootstrapModelForm):
  class Meta:
    model = Exam
    exclude = ('professor',)

@login_required
def make(request):
  '''Prof makes essay. Includes both 'pages' of the process'''
  client = docAuth()
  message = ''
  if request.method == 'POST':
    exams = Exam.objects.filter(name=request.POST.get('exam_name'))
    if len(exams) == 0:
      return info_submit(request)
    else: 
      message = 'Sorry, there is already an exam named "%s." Please choose another name.' % (request.POST.get('exam_name'))
  context = {
    'message': message,
    'user': request.user,
    }
  return render_to_response('make.html', RequestContext(request, context))

def info_submit(request):
  '''Creates the Essay given a name and start/end time'''
  if request.method == 'POST':
    post = request.POST
    client = docAuth()
    
    date_format = '%m/%d%/%Y'
    time_format = '%I:%M%p'
    #if len(post.get('start_time')) == 6:
    #  start_time = '0'+post.get('start_time')
    #else:
    #  end_time = post.get('end_time')
    #logging.warning(start_time)
    ##if len(post.get('end_time')) == 6:
     # end_time = '0'+post.get('end_time')
    #else:
    #  start_time = post.get('start_time')
    #logging.warning(end_time)
    ##datetime_format = date_format+'-'+time_format
    #start = post.get('start_date')+'-'+post.get('start_time')
    #start_datetime = start_datetime = datetime.datetime(
    #        int(start[0:4]),
     #       int(start[5:7]),
     #       int(start[8:10]),
     #       int(start[11:13]),
      #      int(start[14:16])
      #      )
    #logging.warning(start_datetime)
    #end = post.get('end_date')+'-'+end_time
    #end_datetime = end_datetime = datetime.datetime(
    #        int(end[0:4]),
    #        int(end[5:7]),
    #        int(end[8:10]),
    #        int(end[11:13]),
    #        int(end[14:16])
    #        )
    prof = Professor.objects.get(user=request.user)
    exam_name = post.get('exam_name')
    exam = Exam()
    exam.professor = prof
    exam.name = exam_name
    
    #exam.start_time = start_datetime
    exam.start_time = datetime.datetime.now()
    exam.end_time = datetime.datetime.now()
    new_doc, new_folder = create_doc(request, client, prof, exam_name)
    exam.resource_id = new_doc.resource_id.text
    exam.folder_id = new_folder.resource_id.text
    #try: 
    #  exam.box_fid = createSubFolder(prof.box_id, exam_name)
    #except: 
    #  exam.box_fid = createSubFolder(prof.box_id, exam_name+'1')
    #element = getBox('toggle_folder_email', {'folder_id':exam.folder_id, 'enable':'1'})
    #sexam.box_email = getText(element, 'upload_email')
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
  send_app_email(add_email, subject, msg, attachments)
  logging.warning("sent"+str(attachments))
  return 1

def take(request, exam_name, student_name, student_email):
  client = docAuth()
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
  essay = Essay()
  essay.student_name = student_name
  essay.student_email = student_email
  essay.resource_id = student_doc.resource_id.text
  essay.exam = exam
  essay.start_date = datetime.datetime.now()
  essay.save()
  context = {
    'doc': str(student_doc.resource_id.text).split(':')[1],
    'essay': essay,
    'exam': exam,
  }
  return render_to_response('take.html', RequestContext(request, context))

@login_required
def dashboard(request):
  prof = Professor.objects.get(user=request.user)
  box_id = prof.box_id(name, id)
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
  doc = str(exam.resource_id).split(':')[1]
  context = {
    'exam': exam, 
    'doc': doc,
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
    folder = client.GetDocList(uri='/feeds/default/private/full/-/folder/?title=%s&title-exact=true&max-results=1' % (exam_name)).entry[0]
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
      client = docAuth()
      main_folder = client.Create(gdata.docs.data.FOLDER_LABEL, 'EssaySafe | '+request.POST['email'])
      prompts_folder = client.Create(gdata.docs.data.FOLDER_LABEL, 'Prompts')
      client.Move(prompts_folder, main_folder)
      prof.folder_id = main_folder.resource_id.text
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

def done(request, essay_id):
  essay = get_object_or_404(Essay, id=essay_id)
  exam = essay.exam
  doc = str(essay.resource_id).split(':')[1]
  context = {'doc':doc, 'essay': essay, 'exam':exam, }
  return render_to_response('done.html', context)
