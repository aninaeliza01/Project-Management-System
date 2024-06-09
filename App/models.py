from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    
    username = models.CharField(max_length=50, unique=True)
    is_builder = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class Builder(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, blank=True)
    contact_info = models.CharField(max_length=100, blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    area_of_expertise = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.company_name or 'Independent'})"
    
class Client(models.Model):

  name = models.CharField(max_length=255)
  email = models.EmailField()
  phone_number = models.CharField(max_length=20, blank=True)
  address = models.TextField(blank=True)
  builder=models.ForeignKey(Builder, on_delete=models.CASCADE)

  def __str__(self):
    return self.name
  
class Project(models.Model):
 
  name = models.CharField(max_length=255)
  description = models.TextField(blank=True)
  client = models.ForeignKey(Client, on_delete=models.CASCADE)  
  start_date = models.DateField(blank=True, null=True)
  end_date = models.DateField(blank=True, null=True)
  builder=models.ForeignKey(Builder, on_delete=models.CASCADE)
  STATUS_CHOICES = (
        ('Planning', 'Planning'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    )
  status = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True, null=True)
  budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
  def get_status_choices(self):
    return self.STATUS_CHOICES

