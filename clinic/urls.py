from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', views.login_page),
    path('logout/', views.logout_page),

    path('', views.home),

    path('add/', views.add_patient),
    path('patients/', views.view_patients),

    path('appointment/add/', views.add_appointment),
    path('appointments/', views.view_appointments),
    path('bill/add/', views.add_bill),
path('bills/', views.view_bills),
path('bill/pdf/<int:bill_id>/', views.generate_pdf),
path('report/add/', views.add_report),
path('reports/', views.view_reports),
path('create-admin/', views.create_admin),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)