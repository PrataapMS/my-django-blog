from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
    url(r'^sms/$', views.analyse_sms, name='analyse_sms'),
    url(r'^form/$', views.model_form_upload, name='model_form_upload'),
    url(r'^transactions/$', views.display_transactions, name='display_transactions'),
]	