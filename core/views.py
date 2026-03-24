from django.shortcuts import render, redirect
from .models import Patient, Appointment,Billing,LabReport,Prescription,Patient
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from reportlab.pdfgen import canvas
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PatientSerializer
import json


# LOGIN
def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Invalid Credentials'})

    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect('/login')


# HOME
@login_required
def home(request):
    return render(request, 'home.html')


# ADD PATIENT
@login_required
def add_patient(request):
    if request.method == 'POST':
        Patient.objects.create(
            name=request.POST['name'],
            age=request.POST['age'],
            phone=request.POST['phone']
        )
        return redirect('/patients')

    return render(request, 'add_patient.html')


# VIEW PATIENTS
@login_required
def view_patients(request):
    patients = Patient.objects.all()
    return render(request, 'view_patients.html', {'patients': patients})


# ADD APPOINTMENT
@login_required
def add_appointment(request):
    if request.method == 'POST':
        time = request.POST.get('time')

        if not time:
            return render(request, 'add_appointment.html', {
                'patients': Patient.objects.all(),
                'error': 'Please select time'
            })

        Appointment.objects.create(
            patient=Patient.objects.get(id=request.POST['patient']),
            date=request.POST['date'],
            time=time
        )
        return redirect('/appointments')

    return render(request, 'add_appointment.html', {
        'patients': Patient.objects.all()
    })


# VIEW APPOINTMENTS
@login_required
def view_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'view_appointments.html', {'appointments': appointments})

@login_required
def add_bill(request):
    if request.method == 'POST':
        Billing.objects.create(
            patient=Patient.objects.get(id=request.POST['patient']),
            amount=request.POST['amount'],
            description=request.POST['description']
        )
        return redirect('/bills')

    patients = Patient.objects.all()
    return render(request, 'add_bill.html', {'patients': patients})    

@login_required
def view_bills(request):
    bills = Billing.objects.all()
    return render(request, 'view_bills.html', {'bills': bills})

def generate_bill_pdf(request, bill_id):
    bill = Billing.objects.get(id=bill_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    p = canvas.Canvas(response)

    p.drawString(100, 800, "Clinic Invoice")
    p.drawString(100, 770, f"Patient: {bill.patient.name}")
    p.drawString(100, 750, f"Amount: {bill.amount}")
    p.drawString(100, 730, f"Description: {bill.description}")
    p.drawString(100, 710, f"Date: {bill.date}")

    p.save()
    return response

@login_required
def add_report(request):
    if request.method == 'POST':
        LabReport.objects.create(
            patient=Patient.objects.get(id=request.POST['patient']),
            report_name=request.POST['report_name'],
            file=request.FILES['file']
        )
        return redirect('/reports')

    patients = Patient.objects.all()
    return render(request, 'add_report.html', {'patients': patients})

@login_required
def view_reports(request):
    reports = LabReport.objects.all()
    return render(request, 'view_reports.html', {'reports': reports})

def create_admin(request):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@gmail.com", "1234")
        return HttpResponse("Admin created")
    return HttpResponse("Already exists")

@login_required
def view_patients(request):
    query = request.GET.get('q')
    
    if query:
        patients = Patient.objects.filter(name__icontains=query)
    else:
        patients = Patient.objects.all()

    return render(request, 'view_patients.html', {'patients': patients})

@login_required
def add_prescription(request):
    if request.method == 'POST':
        Prescription.objects.create(
            patient=Patient.objects.get(id=request.POST['patient']),
            doctor_name=request.POST['doctor'],
            medicine=request.POST['medicine'],
            notes=request.POST['notes']
        )
        return redirect('/prescriptions')

    patients = Patient.objects.all()
    return render(request, 'add_prescription.html', {'patients': patients})

@login_required
def view_prescriptions(request):
    prescriptions = Prescription.objects.all()
    return render(request, 'view_prescriptions.html', {'prescriptions': prescriptions})

from django.db.models import Sum

@login_required
def home(request):
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.count()
    total_revenue = Billing.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'home.html', {
        'patients': total_patients,
        'appointments': total_appointments,
        'revenue': total_revenue
    })

def generate_prescription_pdf(request, id):
    p = Prescription.objects.get(id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="prescription.pdf"'

    c = canvas.Canvas(response)

    c.drawString(100, 800, "Clinic Prescription")
    c.drawString(100, 770, f"Patient: {p.patient.name}")
    c.drawString(100, 750, f"Doctor: {p.doctor_name}")
    c.drawString(100, 730, f"Medicine: {p.medicine}")
    c.drawString(100, 710, f"Notes: {p.notes}")

    c.save()
    return response

def is_doctor(user):
    return user.profile.role == 'doctor'

@api_view(['GET'])
def api_patients(request):
    patients = Patient.objects.all()
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        return Response({
            "status": "success",
            "message": "Login successful"
        })
    else:
        return Response({
            "status": "error",
            "message": "Invalid credentials"
        })

def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({"status": "error", "message": "Invalid JSON"})

        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({
                "status": "error",
                "message": "Invalid username or password"
            })

    return JsonResponse({"status": "error", "message": "Only POST allowed"})

def logout_view(request):
    logout(request)
    return redirect('/login/')