from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
import datetime
from django.db.models.signals import post_save
from django.core.files import File
import os.path
import djangotoolbox.fields as models2
from django.template.defaultfilters import slugify
from oauth2client.django_orm import FlowField
from oauth2client.django_orm import CredentialsField

class Professor(models.Model):
  """ 
  Professor model.
  """
  name = models.CharField(max_length=80)
  
  def __unicode__(self):
    return self.name
  
class Exam(models.Model):
  """ Exam model.
  """
  exam_name = models.CharField(max_length=80)
  
  def __unicode__(self):
    return self.name

class Essay(models.Model):
  exam = models.ForeignKey(Exam)
  student_name = models.CharField(max_length=80)
  begin_date = models.DateTimeField('date started')
  end_date = models.DateTimeFiled('date finished')

class Doc(models.Model):
  doc_name = models.CharField(max_length=80)
  resource_id_text = models.CharField(max_length=80)

class FlowModel(models.Model):
  id = models.ForeignKey(User, primary_key=True)
  flow = FlowField()

class CredentialsModel(models.Model):
  id = models.ForeignKey(User, primary_key=True)
  credential = CredentialsField()


class CredentialsAdmin(admin.ModelAdmin):
  pass

class FlowAdmin(admin.ModelAdmin):
  pass


admin.site.register(CredentialsModel, CredentialsAdmin)
admin.site.register(FlowModel, FlowAdmin)
