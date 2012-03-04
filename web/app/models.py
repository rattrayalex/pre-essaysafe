from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
import datetime
from django.db.models.signals import post_save
from django.core.files import File
import os.path
import djangotoolbox.fields as models2
from django.template.defaultfilters import slugify


class Professor(models.Model):
  """ 
  Professor model.
  """
  email = models.CharField(max_length=80)
  box_id = models.CharField()
  gdocs_id = models.CharField()
  user = models.OneToOneField(User, unique=True)
  name = models.CharField()
  folder_id = models.CharField(max_length=80, blank=True)
  token = models.CharField(max_length=100, blank=True)
  token_secret = models.CharField(max_length=100, blank=True)
  ##auth_token = models.CharField(max_length=100, blank=True)
  
  def __unicode__(self):
    return self.name
  
class Exam(models.Model):
  """ Exam model.
  """
  professor = models.ForeignKey(Professor, null=True)
  name = models.CharField(max_length=80, unique=True)
  start_time = models.DateTimeField(blank=True)
  end_time = models.DateTimeField(blank=True)
  resource_id = models.CharField(max_length=80)
  folder_id = models.CharField(max_length=80)
  box_fid = models.CharField(max_length=100)
  box_email = models.CharField(max_length=100)
  
  def __unicode__(self):
    return self.name

class Essay(models.Model):
  exam = models.ForeignKey(Exam)
  student_name = models.CharField(max_length=80)
  begin_date = models.DateTimeField('date started')
  end_date = models.DateTimeField('date finished')
  latitude = models.DecimalField()
  longitude = models.DecimalField()
  resource_id = models.CharField()

class Doc(models.Model):
  doc_name = models.CharField(max_length=80)
  resource_id = models.CharField(max_length=80)

