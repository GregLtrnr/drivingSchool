from django.db import models

# Create your models here.
class Account(models.Model):
  ACCOUNT_TYPES = (
    ('student', 'Student'),
    ('instructor', 'Instructor'),
    ('secretary', 'Secretary'),
    ('admin', 'Admin'),
  )

  id = models.AutoField(primary_key=True)
  account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  date_of_birth = models.DateField()
  address = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)
  user = models.OneToOneField('auth.User', on_delete=models.CASCADE) 
  paid_hours = models.IntegerField(default=0)

  def __str__(self):
    return f"{self.first_name} {self.last_name}"

class Appointment(models.Model):
  id = models.AutoField(primary_key=True)
  date_start = models.DateTimeField()
  date_end = models.DateTimeField()
  location = models.CharField(max_length=100)
  instructor = models.ForeignKey(
    Account, related_name='instructor_appointments', on_delete=models.CASCADE,
    limit_choices_to={'account_type': 'instructor'}
  )
  student = models.ForeignKey(
    Account, related_name='student_appointments', on_delete=models.CASCADE,
    limit_choices_to={'account_type': 'student'}
  )

  def __str__(self):
    return f'Appointment {self.id} - {self.student.first_name} {self.student.last_name} with {self.instructor.first_name} {self.instructor.last_name}'

  class Meta:
    verbose_name = 'Appointment'
    verbose_name_plural = 'Appointments'
    ordering = ['-date_start']
