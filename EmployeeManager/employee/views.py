from django.shortcuts import render
from django.core.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from EmployeeManager.utils.pagination import CustomPagination
from employee.serializers import EmployeeSerializer, EmployeeReadSerializer
from employee.models import EmployeeModel


class CreateEmployee(generics.CreateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()


class ListEmployee(generics.ListAPIView):
    serializer_class = EmployeeReadSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get_queryset(self):
        return EmployeeModel.objects.all()


class DeleteEmployee(generics.DestroyAPIView):
    serializer_class = EmployeeReadSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        try:
            return EmployeeModel.objects.get(
                external_id=self.kwargs.get("external_id")
            )
        except (EmployeeModel.DoesNotExist, ValidationError):
            raise NotFound("Employee does not exist")
    
    def delete(self, request, *args, **kwargs):
        super(DeleteEmployee, self).delete(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateEmployee(generics.UpdateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        try:
            return EmployeeModel.objects.get(
                external_id=self.kwargs.get("external_id")
            )
        except (EmployeeModel.DoesNotExist, ValidationError):
            raise NotFound("Employee does not exist")


class GetEmployee(generics.RetrieveAPIView):
    serializer_class = EmployeeReadSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        try:
            return EmployeeModel.objects.get(
                external_id=self.kwargs.get("external_id")
            )
        except (EmployeeModel.DoesNotExist, ValidationError):
            raise NotFound("Employee does not exist")
