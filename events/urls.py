from django.contrib import admin
from django.urls import path, include, re_path
from . import views

admin.AdminSite.site_header = 'All1Zed Events Tickets'
admin.AdminSite.site_title = 'All1Zed Events Tickets'

urlpatterns = [
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('', views.index, name='index')
]