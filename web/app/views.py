from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from google.appengine.ext import db

from django.conf import settings
from django.utils.importlib import import_module
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import gdata.auth
import gdata.docs.data
import gdata.docs.client
import gdata.docs.service

from app.models import *
import os, sys, datetime, copy, logging, settings

STEP2_URI = 'https://beta.essaysafe.org/oauth2callback'

# Change everything in this class! Makes things pretty fast and easy
# so the basic info about the site is ubiquitous. 

CLIENT_ID = '1075895061839-air2l59at4t8gsng9ml8a3j0qspfp8i8.apps.googleusercontent.com'
CLIENT_SECRET = '6savVHl6blxgIwodzBRKXPMc'

class SampleConfig(object):
  APP_NAME = 'essaysafe-essaysafe-v0.1'
  DEBUG = True

class OAuthSample(object):
  """Sample class demonstrating the three-legged OAuth process."""

  def __init__(self, consumer_key, consumer_secret):
    """Constructor for the OAuthSample object.
    
    Takes a consumer key and consumer secret, store them in class variables,
    creates a DocsService client to be used to make calls to
    the Documents List Data API.
    
    Args:
      consumer_key: string Domain identifying third_party web application.
      consumer_secret: string Secret generated during registration.
    """
    self.consumer_key = CLIENT_ID
    self.consumer_secret = CLIENT_SECRET
    self.gd_client = gdata.docs.service.DocsService()

  def _PrintFeed(self, feed):
    """Prints out the contents of a feed to the console.
   
    Args:
      feed: A gdata.docs.DocumentListFeed instance.
    """
    if not feed.entry:
      print 'No entries in feed.\n'
    
    docs_list = list(enumerate(feed.entry, start = 1))
    for i, entry in docs_list:
      print '%d. %s\n' % (i, entry.title.text.encode('UTF-8'))

  def _ListAllDocuments(self):
    """Retrieves a list of all of a user's documents and displays them."""
    feed = self.gd_client.GetDocumentListFeed()
    self._PrintFeed(feed)
    
  def Run(self):
    """Demonstrates usage of OAuth authentication mode and retrieves a list of
    documents using the Document List Data API."""
    print '\nSTEP 1: Set OAuth input parameters.'
    self.gd_client.SetOAuthInputParameters(
        gdata.auth.OAuthSignatureMethod.HMAC_SHA1,
        self.consumer_key, consumer_secret=self.consumer_secret)
    print '\nSTEP 2: Fetch OAuth Request token.'
    request_token = self.gd_client.FetchOAuthRequestToken()
    print 'Request Token fetched: %s' % request_token
    print '\nSTEP 3: Set the fetched OAuth token.'
    self.gd_client.SetOAuthToken(request_token)
    print 'OAuth request token set.'
    print '\nSTEP 4: Generate OAuth authorization URL.'
    auth_url = self.gd_client.GenerateOAuthAuthorizationURL()
    print 'Authorization URL: %s' % auth_url
    raw_input('Manually go to the above URL and authenticate.'
              'Press a key after authorization.')
    print '\nSTEP 5: Upgrade to an OAuth access token.'
    self.gd_client.UpgradeToOAuthAccessToken()
    print 'Access Token: %s' % (
        self.gd_client.token_store.find_token(request_token.scopes[0]))
    print '\nYour Documents:\n'
    self._ListAllDocuments()
    print 'STEP 6: Revoke the OAuth access token after use.'
    self.gd_client.RevokeOAuthToken()
    print 'OAuth access token revoked.'


def main():
  sample = OAuthSample(CLIENT_ID, CLIENT_SECRET)
  sample.Run()


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

def make(request):
  sample = OAuthSample(CLIENT_ID, CLIENT_SECRET)
  sample.Run()
  feed = self.gd_client.GetDocumentListFeed()
##  client = CreateClient()
##  feed = client.GetDocList(limit = 10)
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
