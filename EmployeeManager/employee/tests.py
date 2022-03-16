from urllib import request
import uuid
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from employee.models import EmployeeModel


# Create your tests here.
class TestE2EEmployee(APITestCase):
    
    def assert_is_uuid(self, data):
        try:
           uuid.UUID(data) 
        except ValueError:
            self.fail("Invalud UUID")

    def test_create_employee__expected_employee_created(self):
        endpoint = "/employee/create"
        data = {
            "name": "teste",
            "email": "teste@email.com",
            "department": "departamento de teste"
        }

        response = self.client.post(endpoint, data, format='json')
        
        employee_created = EmployeeModel.objects.get(
            name="teste",
            email="teste@email.com",
            department="departamento de teste"
        )

        assert response.status_code == 201
        assert ['external_id', 'registration_date', 'name', 'email', 'department'] == list(response.data.keys())
        assert response.data.get("name") == "teste"
        assert response.data.get("email") == "teste@email.com"
        assert response.data.get("department") == "departamento de teste"
        self.assert_is_uuid(data=response.data.get("external_id"))
        assert employee_created.name == "teste"
        assert employee_created.email == "teste@email.com"
        assert employee_created.department == "departamento de teste"
        assert employee_created.registration_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ") == response.data.get("registration_date")

    def test_create_employee__expected_email_validation_error(self):
        endpoint = "/employee/create"
        data = {
            "name": "teste",
            "email": "teste.email-invalido.com",
            "department": "departamento de teste"
        }

        response = self.client.post(endpoint, data, format='json')
        
        with self.assertRaises(EmployeeModel.DoesNotExist):
            EmployeeModel.objects.get(
                name="teste",
                email="teste.email-invalido.com",
                department="departamento de teste"
            )
        assert response.status_code == 400
        assert isinstance(response.data.get("email"), list)
        assert str(response.data.get("email")[0]) == "Enter a valid email address."
        assert "email" in response.data.keys()
    
    def test_delete_employee__expected_employee_deleted(self):
        employee = EmployeeModel.objects.create(
            name="teste",
            email="teste@email.com",
            department="departamento de teste"
        )
        endpoint = f"/employee/delete/{employee.external_id}"

        response = self.client.delete(endpoint, format='json')
        
        assert response.status_code == 204

        with self.assertRaises(EmployeeModel.DoesNotExist):
            EmployeeModel.objects.get(
                name="teste",
                email="teste@email.com",
                department="departamento de teste"
            )

    def test_delete_employee__expected_employee_not_found(self):
        endpoint = "/employee/delete/866bc97d-10fc-4682-9ddf-9d97efdf000e"

        response = self.client.delete(endpoint, format='json')
        
        assert response.status_code == 404
        assert response.data.get('detail').code == "not_found"
        assert str(response.data.get('detail')) == "Employee does not exist"

    def test_update_employee__expected_put_employee(self):
        employee = EmployeeModel.objects.create(
            name="teste",
            email="teste@email.com",
            department="departamento de teste"
        )
        endpoint = f"/employee/update/{employee.external_id}"
        data = {
            "name": "teste2",
            "email": "teste2@email.com",
            "department": "departamento de teste2"
        }

        response = self.client.put(endpoint, data, format='json')

        employee_created = EmployeeModel.objects.get(
            name="teste2",
            email="teste2@email.com",
            department="departamento de teste2"
        )

        assert response.status_code == 200
        assert ['external_id', 'registration_date', 'name', 'email', 'department'] == list(response.data.keys())
        assert response.data.get("name") == "teste2"
        assert response.data.get("email") == "teste2@email.com"
        assert response.data.get("department") == "departamento de teste2"
        self.assert_is_uuid(data=response.data.get("external_id"))
        assert employee_created.name == "teste2"
        assert employee_created.email == "teste2@email.com"
        assert employee_created.department == "departamento de teste2"
        assert employee_created.registration_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ") == response.data.get("registration_date")

    def test_update_employee__expected_put_employee_with_only_one_fild_to_att(self):
        employee = EmployeeModel.objects.create(
            name="teste",
            email="teste@email.com",
            department="departamento de teste"
        )
        endpoint = f"/employee/update/{employee.external_id}"
        data = {
            "name": "teste2",
        }

        response = self.client.put(endpoint, data, format='json')

        with self.assertRaises(EmployeeModel.DoesNotExist):
            EmployeeModel.objects.get(
                name="teste2",
                email="teste@email.com",
                department="departamento de teste2"
            )
        assert response.status_code == 400
        assert str(response.data.get("email")[0]) == "This field is required."
        assert response.data.get("email")[0].code == "required"
        assert isinstance(response.data.get("email"), list)
        assert str(response.data.get("department")[0]) == "This field is required."
        assert response.data.get("department")[0].code == "required"
        assert isinstance(response.data.get("department"), list)

    def test_update_employee__expected_put_employee_with_invalid_email(self):
        employee = EmployeeModel.objects.create(
            name="teste",
            email="teste@email.com",
            department="departamento de teste"
        )
        endpoint = f"/employee/update/{employee.external_id}"
        data = {
            "name": "teste2",
            "email": "teste2.email-invalido.com",
            "department": "departamento de teste2"
        }

        response = self.client.put(endpoint, data, format='json')

        assert response.status_code == 400
        assert isinstance(response.data.get("email"), list)
        assert response.data.get("email")[0].code == "invalid"
        assert str(response.data.get("email")[0]) == "Enter a valid email address."

    def test_update_employee__expected_patch_employee(self):
        employee = EmployeeModel.objects.create(
            name="teste",
            email="teste@email.com",
            department="departamento de teste"
        )
        endpoint = f"/employee/update/{employee.external_id}"
        data = {
            "email": "teste2@email.com"
        }

        response = self.client.patch(endpoint, data, format='json')

        employee_created = EmployeeModel.objects.get(
            name="teste",
            email="teste2@email.com",
            department="departamento de teste"
        )

        assert response.status_code == 200
        assert ['external_id', 'registration_date', 'name', 'email', 'department'] == list(response.data.keys())
        assert response.data.get("name") == "teste"
        assert response.data.get("email") == "teste2@email.com"
        assert response.data.get("department") == "departamento de teste"
        self.assert_is_uuid(data=response.data.get("external_id"))
        assert employee_created.name == "teste"
        assert employee_created.email == "teste2@email.com"
        assert employee_created.department == "departamento de teste"
        assert employee_created.registration_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ") == response.data.get("registration_date")

    def test_update_employee__expected_patch_employee_with_invalid_email(self):
        employee = EmployeeModel.objects.create(
            name="teste",
            email="teste@email.com",
            department="departamento de teste"
        )
        endpoint = f"/employee/update/{employee.external_id}"
        data = {
            "email": "teste2.email-invalido.com"
        }

        response = self.client.patch(endpoint, data, format='json')

        assert response.status_code == 400
        assert isinstance(response.data.get("email"), list)
        assert response.data.get("email")[0].code == "invalid"
        assert str(response.data.get("email")[0]) == "Enter a valid email address."

    def test_list_employee__expected_employee_list(self):
        employee = [
            EmployeeModel.objects.create(
                name="teste1",
                email="teste1@email.com",
                department="departamento de teste1"
            ),
            EmployeeModel.objects.create(
                name="teste2",
                email="teste2@email.com",
                department="departamento de teste2"
            )
        ]
        endpoint = "/employee/list"
        data = {
            "email": "teste2.email-invalido.com"
        }

        response = self.client.get(endpoint, data, format='json')

        assert response.status_code == 200
        assert not response.data['next']
        assert not response.data['previous']
        assert len(response.data['results']) == 2
        assert isinstance(response.data['results'], list)

        assert response.data['results'][0].get("name") == "teste1"
        assert response.data['results'][0].get("email") == "teste1@email.com"
        assert response.data['results'][0].get("department") == "departamento de teste1"
        assert ['external_id', 'registration_date', 'name', 'email', 'department'] == list(response.data['results'][0].keys())
        assert employee[0].registration_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ") == response.data['results'][0].get("registration_date")
        self.assert_is_uuid(
            data=response.data['results'][0].get("external_id")
        )

        assert response.data['results'][1].get("name") == "teste2"
        assert response.data['results'][1].get("email") == "teste2@email.com"
        assert response.data['results'][1].get("department") == "departamento de teste2"
        assert ['external_id', 'registration_date', 'name', 'email', 'department'] == list(response.data['results'][1].keys())
        assert employee[1].registration_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ") == response.data['results'][1].get("registration_date")
        self.assert_is_uuid(
            data=response.data['results'][1].get("external_id")
        )

    def test_get_employee__expected_employee_detail(self):
        employee = EmployeeModel.objects.create(
            name="teste",
            email="teste@email.com",
            department="departamento de teste"
        )
        endpoint = f"/employee/detail/{employee.external_id}"
        data = {
            "email": "teste2.email-invalido.com"
        }

        response = self.client.get(endpoint, data, format='json')

        assert response.status_code == 200
        assert ['external_id', 'registration_date', 'name', 'email', 'department'] == list(response.data.keys())
        assert response.data.get("name") == "teste"
        assert response.data.get("email") == "teste@email.com"
        assert response.data.get("department") == "departamento de teste"
        self.assert_is_uuid(data=response.data.get("external_id"))
        assert employee.registration_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ") == response.data.get("registration_date")

    def test_get_employee__expected_employee_not_found(self):
        endpoint = "/employee/detail/866bc97d-10fc-4682-9ddf-9d97efdf000e"

        response = self.client.get(endpoint, format='json')

        assert response.status_code == 404
        assert response.data.get('detail').code == "not_found"
        assert str(response.data.get('detail')) == "Employee does not exist"
