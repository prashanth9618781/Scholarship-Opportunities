from django.db import models
from django.contrib.auth.models import User

# Scholarship Model
class Scholarship(models.Model):
    title = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    description = models.TextField()
    eligibility_criteria = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    application_deadline = models.DateField()
    academic_level = models.CharField(max_length=100, choices=[
        ('high_school', 'High School'),
        ('undergraduate', 'Undergraduate'),
        ('postgraduate', 'Postgraduate'),
        ('phd', 'PhD'),
    ])
    field_of_study = models.CharField(max_length=255, blank=True, null=True)
    min_gpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    location_restriction = models.CharField(max_length=255, blank=True, null=True)
    financial_need_required = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# Scholarship Application Model
class ScholarshipApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
        ('under_review', 'Under Review'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"{self.student.full_name} - {self.scholarship.title} ({self.status})"
