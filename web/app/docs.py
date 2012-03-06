import gdata.docs.data
import gdata.docs.client

APP_NAME = 'essaysafe-essaysafe-v0.1'
APP_EMAIL = 'essay.safe.hack@gmail.com'
APP_PASS = 'angelhack'

def glogin():
  '''Authenticates with Google Docs'''
  client = gdata.docs.client.DocsClient()
  auth_token = client.ClientLogin(APP_EMAIL, APP_PASS, APP_NAME)
  return client

def create_folder(folder, parent_folder=None):
  folder = client.Create(gdata.gdata.data.FOLDER_LABEL, folder, folder_or_id=parent_folder)
  return folder.resource_id.text


if __name__ == 'main':
  client = glogin()
