from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class UserAdmin(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    password = models.CharField(max_length=100)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']
    def __str__(self):
        return self.email
    
class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True, unique=True)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=254)
    phone = models.CharField(max_length=20)
    birthday = models.DateField()
    address = models.CharField(max_length=120)
    salary = models.IntegerField()
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    position = models.ForeignKey('Position', on_delete=models.CASCADE)
    join_date = models.DateField()
    primes = models.ManyToManyField('TypePrime', through='Prime')
    
    def __str__(self):
        return self.fullname
    def toJson(self):
        return {
            'fullname': self.fullname,
            'email': self.email,
            'phone': self.phone,
            'birthday': 'today',
            'address': self.address,
            'salary': self.salary,
        }

class Department(models.Model):
    department_id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Position(models.Model):
    position_id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class TypePrime(models.Model):
    type_prime_id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    money = models.IntegerField()
    
    def __str__(self):
        return self.name

class Prime(models.Model):
    prime_id = models.AutoField(primary_key=True, unique=True)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    type_prime = models.ForeignKey('TypePrime', on_delete=models.CASCADE)
    date = models.DateField()
    
    def __str__(self):
        return self.employee.fullname + " - " + self.type_prime.name
