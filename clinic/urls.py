from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # API
    path('api/patients/', views.api_patients),
    path('api/login/', views.api_login),   # ✅ ADD THIS

    # Auth
    path('login/', views.login_view),
    path('logout/', views.logout_view),

    # Patients
    path('add/', views.add_patient),
    path('patients/', views.view_patients),

    # Appointments
    path('appointment/add/', views.add_appointment),
    path('appointments/', views.view_appointments),

    # Billing
    path('bill/add/', views.add_bill),
    path('bills/', views.view_bills),
    path('bill/pdf/<int:bill_id>/', views.generate_bill_pdf),

    # Reports
    path('report/add/', views.add_report),
    path('reports/', views.view_reports),

    # Prescription
    path('prescription/add/', views.add_prescription),
    path('prescriptions/', views.view_prescriptions),
    path('prescription/pdf/<int:id>/', views.generate_prescription_pdf),

    path('create-admin/', views.create_admin),
]