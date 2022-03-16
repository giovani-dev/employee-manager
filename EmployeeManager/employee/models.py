import uuid
from django.db import models


# employee information, such as name, e-mail and department
class EmployeeModel(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(max_length=254, unique=True)
    department = models.CharField(max_length=150, null=False, blank=False)

    class Meta:
        db_table = "employee"
        verbose_name_plural = "Employee"
