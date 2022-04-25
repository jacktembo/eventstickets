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
    path('events', views.events, name='events'),
    path('<int:pk>/detail', views.event_detail, name='event-detail'),
    path('pay/<event_id>', views.mobile_payment, name='card-payment'),
    path('pay/<event_id>/confirm', views.payment_approval, name='payment-approval'),
    path('payment-waiting', views.payment_waiting, name='payment-waiting'),
    path('<ticket_number>/download', views.DownloadView.as_view(), name='download-ticket'),
    path('ticket', TemplateView.as_view(template_name='ticket.html', extra_context=ticket_context)),
    path('scan', views.scan, name='scan'),
    path('scan/<ticket_number>', views.scan_ticket, name='scan-ticket'),
    path('<int:event_id>/tickets/view', views.tickets_list, name='tickets-view'),
    path('<int:event_id>/tickets/download', views.TicketsListView.as_view(), name='tickets-download'),
    path('payment-success', views.payment_success, name='payment-success'),
    path('generate', views.generate_pdf_ticket),
    path('terms', views.terms, name='terms'),
]
if settings.DEBUG or settings.DEBUG == False:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
