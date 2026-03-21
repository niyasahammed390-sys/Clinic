from django.contrib import admin
from .models import Patient, Appointment, Billing, LabReport

admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Billing)
admin.site.register(LabReport)