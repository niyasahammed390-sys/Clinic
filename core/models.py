from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.patient.name} - {self.date}"

class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    amount = models.FloatField()
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.patient.name

class LabReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    report_name = models.CharField(max_length=100)
    file = models.FileField(upload_to='reports/')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.report_name