from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_save
from django.core.files import File
import os.path
import djangotoolbox.fields as models2
from django.template.defaultfilters import slugify

#check the docs for examples. 
#there are a few weirdnesses about using django-appengine, 
#especially handling dynamic images/files. We do that in the docs. 
