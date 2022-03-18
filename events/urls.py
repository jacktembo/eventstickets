from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

ticket_context = {}

admin.AdminSite.site_header = 'All1Zed Events Tickets'
admin.AdminSite.site_title = 'All1Zed Events Tickets'

urlpatterns = [
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('', views.index, name='index'),
    path('<int:pk>/detail', views.event_detail, name='event-detail'),
    path('pay-with-card/<event_id>', views.card_payment, name='card-payment'),
    path('<ticket_number>/download', views.DownloadView.as_view()),
    path('ticket', TemplateView.as_view(template_name='ticket.html', extra_context=ticket_context)),
    path('scan', views.scan, name='scan'),
]
if settings.DEBUG or settings.DEBUG == False:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
