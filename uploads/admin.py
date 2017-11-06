# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Document, Transactions


class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'sent_by', 'card_id', 'amount', 'trans_date', 'msg_recv_date', )

# Register your models here.
admin.site.register(Document)
admin.site.register(Transactions, TransactionsAdmin)