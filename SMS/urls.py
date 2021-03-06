from django.urls import path
from django.conf.urls import url
from django.conf import settings
# from django.views.static import serve
from django.conf.urls.static import static
from SMS.views import pdf_report


from . import views

# app_name = 'SMS'
urlpatterns = [
    path('', views.index, name='index'),
    path('cert_remove/<int:cert>', views.cert_remove, name='cert_remove'),
    path('cert_edit/<int:cert>', views.cert_edit, name='cert_edit'),
    path('base_data/<int:company_id>', views.base_data, name='base_data'),
    path('certs/<int:company_id>', views.certs, name='certs'),
    path('user_activate/<int:user_Nb>/', views.user_activate, name='user_activate'),
    path('claims/<int:company_id>/', views.claims, name='claims'),
    path('tasks/<int:company_id>/', views.tasks, name='tasks'),
    path('claim_remove/<int:claim>/', views.claim_remove, name='claim_remove'),
    path('claim_edit/<int:claim>/', views.claim_edit, name='claim_edit'),
    path('claim_Data/<int:claim>/', views.D1D8, name='claim_Data'),
    path('D1/<int:claim>/', views.D1D8, name='D1'),
    path('D2/<int:claim>/', views.D1D8, name='D2'),
    path('D3/<int:claim>/', views.D1D8, name='D3'),
    path('D4/<int:claim>/', views.D1D8, name='D4'),
    path('D5/<int:claim>/', views.D1D8, name='D5'),
    path('D6/<int:claim>/', views.D1D8, name='D6'),
    path('D7/<int:claim>/', views.D1D8, name='D7'),
    path('D8/<int:claim>/', views.D1D8, name='D8'),
    path('pdf_report/<int:claim>/', pdf_report.as_view(), name='pdf_report'),
#     path('8D_pdf/<int:claim>/', views.pdf_report, name='pdf_report'),
    path('new_claim/<int:company_id>/', views.new_claim, name='new_claim'),
    path('vendor_new/', views.vendor_new, name='vendor_new'),
    path('vendor_edit/<int:vendor>', views.vendor_edit, name='vendor_edit'),
    path('user_new/<int:company_id>', views.user_new, name='user_new'),
    path('user_edit/<int:user>', views.user_edit, name='user_edit'),
    path('task_tracker/<str:order>/<int:project>/<str:subproject>/<int:id>', views.task_tracker, name='task_tracker'),
    path('task_details/<str:order>/<int:project>/<str:subproject>/<int:id>', views.task_details, name='task_details'),
#     path('task_tracker/<int:project>/<str:subproject>/<int:id>', views.task_tracker, name='task_tracker'),
#     path('userprofile_new/<int:new_user>', views.userprofile_new, name='userprofile_new'),
#     path('admin_new/<int:vendor>', views.user_new, name='user_new'),
#     path('certs/<int:company_id>/', views.certs, name='certs'),
#     path('ppaps/<int:company_id>/', views.ppaps, name='ppaps'),
#     path('claims/', views.claims, name='claims'),
#     path('claims/<int:claim_id>/', views.claim_details, name='claim details'),
#     path('<int:company_id>/', views.base_data, name='base_data'),
]

if settings.DEBUG:
#     urlpatterns += [
#         url(r'^media/(?P<path>.*)$', serve, {
#             'document_root': settings.MEDIA_ROOT,
#         }),
#     ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)