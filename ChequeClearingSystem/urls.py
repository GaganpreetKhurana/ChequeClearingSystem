from django.conf.urls import url

from . import views

app_name = 'ChequeClearingSystem'
'''
list of patterns for url for redirection
'''
urlpatterns = [
    url(r'^register', views.UserFormView.as_view(), name='register'),
    url(r'^profile', views.details, name='profile'),
    url(r'^new_account', views.createAccountHolder, name='new_account'),
    url(r'^', views.LoginFormView.as_view(), name='main'),
    url(r'^logout', views.logout_view, name='logout'),

]
