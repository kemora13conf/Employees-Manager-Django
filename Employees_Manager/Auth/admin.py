from django.contrib import admin

# Register your models here.
admin.site.site_header = "Employees Manager"
admin.site.site_title = "Employees Manager"
admin.site.index_title = "Welcome to Employees Manager"

from .models import UserAdmin, Employee, Department, Position, TypePrime, Prime
admin.site.register(UserAdmin)
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(TypePrime)
admin.site.register(Prime)

