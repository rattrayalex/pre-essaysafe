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
  '''Professor model.'''
  email = models.CharField(max_length=80, unique=True)
  # gdocs_id = models.CharField(max_length=100)
  user = models.OneToOneField(User, unique=True, related_name='professor')
  name = models.CharField(max_length=100, blank=True)
  folder_id = models.CharField(max_length=80)
  
  def __unicode__(self):
    return self.name
  
class Exam(models.Model):
  ''' Exam model.'''
  professor = models.ForeignKey(Professor)
  name = models.CharField(max_length=80)
  day = models.IntegerField(blank=True)
  start_hour = models.IntegerField(blank=True)
  end_hour = models.IntegerField(blank=True)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  resource_id = models.CharField(max_length=80)
  folder_id = models.CharField(max_length=80)
  
  class Meta: 
    unique_together = (('professor','name'),)
  
  def __unicode__(self):
    return self.name

class Essay(models.Model):
  exam = models.ForeignKey(Exam, blank=True, null=True, related_name='exam')
  student_name = models.CharField(max_length=80, blank=True)
  student_email = models.CharField(max_length=80, blank=True)
  start_time = models.DateTimeField('date finished', blank=True, null=True)
  end_time = models.DateTimeField('date finished', blank=True, null=True)
  latitude = models.DecimalField(blank=True, null=True)
  longitude = models.DecimalField(blank=True, null=True)
  resource_id = models.CharField(blank=True, null=True)
  
  @property
  def minutes_late(self):
    exam_end = self.exam.end_time 
    student_end = self.end_time
    difference = exam_end - student_end
    if difference > datetime.timedelta(0): #not sure this is right; might be reverse
      return '%s early' % difference
    else: 
      return '%s late' % difference
      
class Doc(models.Model):
  doc_name = models.CharField(max_length=80)
  resource_id = models.CharField(max_length=80)

