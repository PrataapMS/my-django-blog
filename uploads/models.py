# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Document(models.Model):
	description = models.CharField(max_length=255, blank=True)
	document = models.FileField(upload_to='documents/')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	

class Transactions(models.Model):
	sent_by = models.CharField(max_length=30, blank=False, null=False)
	card_id = models.CharField(max_length=20, blank=False, null=False)
	amount = models.DecimalField(max_digits=13, decimal_places=2, blank=True, null=True)
	trans_date = models.DateTimeField(null=True, blank=True)
	msg_recv_date = models.DateTimeField(null=True, blank=True)
