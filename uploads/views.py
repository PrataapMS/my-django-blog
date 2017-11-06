# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.shortcuts import render
from .forms import DocumentForm
from django.shortcuts import redirect
from .models import Document, Transactions
from django.core.files.storage import FileSystemStorage
from django.utils.encoding import smart_unicode
import re
import datefinder 
from datetime import datetime
from dateutil.parser import parse
from decimal import Decimal
import csv
import json


# Create your views here.
def home(request):
    context = {}
    documents = Document.objects.all()
    context['uploads_home_active']  = True
    context['documents'] = documents
    return render(request, 'core/home.html', context)


def analyse_sms(request):
    context = {}
    context['uploads_home_active']  = True
    validatation_error = True
    if request.method == 'POST' and request.FILES.get('user_messages', False):
        user_messages = request.FILES['user_messages']
        ext = user_messages.name.split('.')
        if(ext and len(ext) > 1 and (ext[-1]=="js" or ext[-1]=="json" or ext[-1]=="txt")):
            all_messages = get_messages(user_messages)
            csv_file = find_credit_info(all_messages)
            if csv_file:
                fs = FileSystemStorage()
                filename = fs.save(user_messages.name, user_messages)
                uploaded_file_url = fs.url(filename)
                context['uploaded_file_url'] = uploaded_file_url
                return render(request, 'core/upload_sms.html', context)
            else:
                validatation_error = True
    if validatation_error:
        context['validatation_error'] = "Please upload file format with <b>.json/.js/.txt</b> with json data of SMS messages"
        return render(request, 'core/upload_sms.html', context)
    return render(request, 'core/upload_sms.html', context)


def model_form_upload(request):
    context = {}
    context['uploads_home_active']  = True
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    context['form'] = form
    return render(request, 'core/model_form_upload.html', context)

def display_transactions(request):
    context = {}
    results = Transactions.objects.all()
    context['results'] = results
    context['display_transaction_active'] = True
    return render(request, 'display/display_transactions.html', context)    

def get_messages(user_messages):
    try:
        message_data = smart_unicode(user_messages.read())
        message_data = message_data[message_data.find('{'): message_data.rfind('}')+1]
        message_data = json.loads(message_data)
        message_data = message_data['messages']
        return message_data
    except Exception as ex:
        print (ex)

def find_credit_info(sms_messages):
    credit_info_list = []
    count = 1
    for sms in sms_messages:

        test_data = {
                        "timestamp": 1492162964004,
                        "datetime": "2017-04-14 15:12:44 IST",
                        "number": "DM-ICICIB",
                        "id": 57,
                        "text": "Tranx of INR 146.00 using Credit Card 4xxx2500 is made at FREECHARGE on 14-APR-17. Avbl Cr lmt:INR 2,11,528.08, Total Cr lmt: INR 2,16,000.00. Tranx of INR 146.00 using Credit Card 4xxx2500 is made at FREECHARGE on 14-APR-17. Avbl Cr lmt:INR 2,11,528.08, Total Cr lmt: INR 2,16,000.00",
                        "mms": False,
                        "sender": False
                    }
        text = sms['text']

        card_pattern = re.compile(r'((\d*[xX]+\d+)|((\d+){3}[xX]*\d*))(\.*)(\s+)')
        card_match = re.findall(card_pattern, text)
        while (isinstance(card_match, list) or isinstance(card_match, tuple)) and len(card_match) > 0:
            card_match = card_match[0]

        sender_pattern = re.compile(r'\b[A-Z]{4,}[a-z]*\b');
        sender_match = re.findall(sender_pattern, text)
        while (isinstance(sender_match, list) or isinstance(sender_match, tuple)) and len(sender_match) > 0:
            sender_match = sender_match[0]

        currency_pattern = re.compile(r'(?:Rs\.?|INR)\s*(\d+(?:[.,]\d+)*)|(\d+(?:[.,]\d+)*)\s*(?:Rs\.?|INR)')
        currency_match = re.findall(currency_pattern, text)
        while (isinstance(currency_match, list) or isinstance(currency_match, tuple)) and len(currency_match) > 0   :
            currency_match = currency_match[0]
        if isinstance(currency_match, str) or isinstance(currency_match, unicode):
            currency_match = currency_match.replace(",", "").replace(" ","")


        # date = '\d{4}[-/]\d{2}[-/]\d{2}'
        date_match = datefinder.find_dates(text)

        for i in date_match:
            if i:
                if i and isinstance(i, datetime):
                    try:
                        date_match = i.strftime("%d-%m-%YT%I:%M:%S%p")
                        break
                    except:
                        continue

        receive_date = sms['datetime']
        receive_date = parse(receive_date)
        receive_date = receive_date.strftime("%d-%m-%YT%I:%M:%S%p")

        if not isinstance(date_match, str):
            date_match =  receive_date

        # S. No. | Sender ID/Number | Credit Card Number (xxxxLast 4 Digit) |  Amount | Transaction Date Time in SMS | SMS Receive Date Time| 
        # e.g. 
        # 1 | HDFCBK| xxxx1234 | 220.5 | 10-Sep-2017 12:15PM | 10-Sep-2017 12:16PM

        if len(credit_info_list) > 0:
            count = len(credit_info_list) + 1

        if sender_match and card_match and currency_match:
            credit_info = {"sno.":count, "send_id": sender_match, "credit_card": card_match, "amount": currency_match, "transaction_date": date_match, "receive_date": receive_date}
            transaction = Transactions(sent_by=sender_match, card_id=card_match, amount=Decimal(currency_match), trans_date=datetime.strptime(date_match, "%d-%m-%YT%I:%M:%S%p"), msg_recv_date=datetime.strptime(receive_date, "%d-%m-%YT%I:%M:%S%p"))
            transaction.save()
            credit_info_list.append(credit_info)

    keys = credit_info_list[0].keys()
    with open('credit.csv', 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(credit_info_list)
        return 'credit.csv'
    return False
