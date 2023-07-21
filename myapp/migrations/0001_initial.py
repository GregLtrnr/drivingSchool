# Generated by Django 4.1.7 on 2023-04-25 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('account_type', models.CharField(choices=[('student', 'Student'), ('instructor', 'Instructor'), ('secretary', 'Secretary'), ('admin', 'Admin')], max_length=20)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('address', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_start', models.DateTimeField()),
                ('date_end', models.DateTimeField()),
                ('location', models.CharField(max_length=100)),
                ('instructor', models.ForeignKey(limit_choices_to={'account_type': 'instructor'}, on_delete=django.db.models.deletion.CASCADE, related_name='instructor_appointments', to='myapp.account')),
                ('student', models.ForeignKey(limit_choices_to={'account_type': 'student'}, on_delete=django.db.models.deletion.CASCADE, related_name='student_appointments', to='myapp.account')),
            ],
            options={
                'verbose_name': 'Appointment',
                'verbose_name_plural': 'Appointments',
                'ordering': ['-date_start'],
            },
        ),
    ]