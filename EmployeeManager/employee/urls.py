"""EmployeeManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from employee.views import (
    CreateEmployee,
    ListEmployee,
    DeleteEmployee,
    UpdateEmployee,
    GetEmployee
)


urlpatterns = [
    path("create", CreateEmployee.as_view(), name="create_employee"),
    path("list", ListEmployee.as_view(), name="list_employee"),
    path("delete/<slug:external_id>", DeleteEmployee.as_view(), name="delete_employee"),
    path("update/<slug:external_id>", UpdateEmployee.as_view(), name="update_employee"),
    path("detail/<slug:external_id>", GetEmployee.as_view(), name="update_employee"),
]
