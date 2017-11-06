from django import forms
from .models import Document, Transactions

class DocumentForm(forms.ModelForm):
    
    class Meta:
        model = Document
        fields = ('description', 'document', )

class TransactionsForm(forms.ModelForm):
    
    class Meta:
        model = Transactions
        fields = ('sent_by', 'card_id', 'amount', 'trans_date', 'msg_recv_date', )
        