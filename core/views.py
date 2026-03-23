from django.shortcuts import render, redirect
from .models import Patient, Appointment,Billing,LabReport
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib.auth.models import User


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

def generate_pdf(request, bill_id):
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
    User.objects.create_superuser('admin', 'admin@gmail.com', 'admin123')
    return HttpResponse("Admin Created")