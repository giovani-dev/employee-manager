from rest_framework import serializers
from employee.models import EmployeeModel


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeModel
        fields = [
            "external_id",
            "registration_date",
            "name",
            "email",
            "department"
        ]
        read_only_fields = [
            "external_id",
            "registration_date"
        ]


class EmployeeReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeModel
        fields = [
            "external_id",
            "registration_date",
            "name",
            "email",
            "department"
        ]
        read_only_fields = [
            "external_id",
            "registration_date",
            "name",
            "email",
            "department"
        ]
