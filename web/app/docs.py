import gdata.docs.data
import gdata.docs.client
from gdata.acl.data import AclScope, AclRole

import logging

APP_NAME = 'essaysafe-essaysafe-v0.1'
APP_EMAIL = 'essay.safe.hack@gmail.com'
APP_PASS = 'angelhack'

def glogin():
  '''Authenticates with Google Docs'''
  client = gdata.docs.client.DocsClient()
  auth_token = client.ClientLogin(APP_EMAIL, APP_PASS, APP_NAME)
  return client

def create_folder(folder_name, parent_folder=None):
  if parent_folder is None:
    return client.Create(gdata.docs.data.FOLDER_LABEL, folder_name)
  else:
    return client.Create(gdata.docs.data.FOLDER_LABEL, folder_name, folder_or_id=parent_folder)

def create_prof_folder(prof_email):
  main_folder = create_folder('EssaySafe | %s' % (prof_email))
  scope = AclScope(value=prof_email, type='user')
  role = AclRole(value='owner')
  acl_entry = gdata.docs.data.Acl(scope=scope, role=role)
  new_acl=client.Post(acl_entry, main_folder.GetAclFeedLink().href)
  create_folder('Prompts', main_folder.resource_id.text)
  return main_folder.resource_id.text

def create_exam(prof_folder_id, exam_name):
  exam_name = 'Prompt | %s' % exam_name
  exam_folder = create_folder(exam_name, prof_folder_id)
  exam_doc = client.Create(gdata.docs.data.DOCUMENT_LABEL, exam_name, folder_or_id=exam_folder)
  return exam_doc.resource_id.text, exam_folder.resource_id.text

def get_files(folder_id):
  uri = 'https://docs.google.com/feeds/default/private/full/%s/contents' % folder_id
  feed = client.GetDocList(uri=uri)
  return [f.title.text for f in feed.entry]

client = glogin()
