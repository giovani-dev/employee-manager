from django.contrib import admin
from employee.models import EmployeeModel


@admin.register(EmployeeModel)
class EmployeeAdmin(admin.ModelAdmin):
    pass
