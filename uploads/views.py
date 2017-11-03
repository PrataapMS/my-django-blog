# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import DocumentForm
from django.shortcuts import redirect
from .models import Document
import re
import datefinder 
from datetime import datetime
from dateutil.parser import parse
import csv


# Create your views here.
def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', { 'documents': documents })


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'core/simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {'form': form})

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
        for i in sms:
            print i, " = " , sms[i]

        card_pattern = re.compile(r'((\d*[xX]+\d+)|((\d+){3}[xX]*\d*))(\.*)(\s+)')
        card_match = re.findall(card_pattern, text)
        while (isinstance(card_match, list) or isinstance(card_match, tuple)) and len(card_match) > 0:
            card_match = card_match[0]

        print card_match

        sender_pattern = re.compile(r'\b[A-Z]{4,}[a-z]*\b');
        sender_match = re.findall(sender_pattern, text)
        print sender_match
        while (isinstance(sender_match, list) or isinstance(sender_match, tuple)) and len(sender_match) > 0:
            sender_match = sender_match[0]
        print sender_match

        currency_pattern = re.compile(r'(?:Rs\.?|INR)\s*(\d+(?:[.,]\d+)*)|(\d+(?:[.,]\d+)*)\s*(?:Rs\.?|INR)')
        currency_match = re.findall(currency_pattern, text)
        while (isinstance(currency_match, list) or isinstance(currency_match, tuple)) and len(currency_match) > 0   :
            currency_match = currency_match[0]
        print currency_match


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
        print receive_date

        if not isinstance(date_match, str):
            date_match =  receive_date
        print date_match

        # S. No. | Sender ID/Number | Credit Card Number (xxxxLast 4 Digit) |  Amount | Transaction Date Time in SMS | SMS Receive Date Time| 
        # e.g. 
        # 1 | HDFCBK| xxxx1234 | 220.5 | 10-Sep-2017 12:15PM | 10-Sep-2017 12:16PM

        if len(credit_info_list) > 0:
            count = len(credit_info_list) + 1

        if sender_match:
            credit_info = {"sno.":count, "send_id": sender_match, "credit_card": card_match, "amount": currency_match, "transaction_date": date_match, "receive_date": receive_date}
            credit_info_list.append(credit_info)
    print credit_info_list

    keys = credit_info_list[0].keys()
    with open('credit.csv', 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(credit_info_list)

