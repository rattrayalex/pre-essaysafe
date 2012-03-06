import gdata.docs.data
import gdata.docs.client
from gdata.acl.data import AclScope, AclRole

APP_NAME = 'essaysafe-essaysafe-v0.1'
APP_EMAIL = 'essay.safe.hack@gmail.com'
APP_PASS = 'angelhack'

def glogin():
  '''Authenticates with Google Docs'''
  client = gdata.docs.client.DocsClient()
  auth_token = client.ClientLogin(APP_EMAIL, APP_PASS, APP_NAME)
  return client

def create_folder(folder_name, parent_folder=None):
  return client.Create(gdata.docs.data.FOLDER_LABEL, folder_name, folder_or_id=parent_folder)

def create_prof_folder(prof_email):
  main_folder = create_folder('EssaySafe | %s' % (prof_email))
  scope = AclScope(value=prof_email, type='user')
  role = AclRole(value='owner')
  acl_entry = gdata.docs.data.Acl(scope=scope, role=role)
  new_acl=client.Post(acl_entry, main_folder.GetAclFeedLink().href)
  create_folder('Prompts', main_folder.resource_id.text)
  return main_folder.resource_id.text


client = glogin()
