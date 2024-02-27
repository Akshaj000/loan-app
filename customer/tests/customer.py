from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from customer.models import Customer


class CustomerRegistrationViewTest(APITestCase):

    def test_register_customer(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 30,
            'monthly_income': 5000,
            'phone_number': '1234567890',
        }

        response = self.client.post('/api/register/', data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Customer.objects.count() ==  1
        
        expected_response_data = {
            'customer_id': Customer.objects.first().customer_id,
            'name': 'John Doe',
            'age': 30,
            'monthly_income': 5000,
            'approved_limit': 180000,
            'phone_number': '1234567890',
        }
        
        assert response.data == expected_response_data

    def test_invalid_data(self):
        invalid_data = {
            'last_name': 'Doe',
            'age': 30,
            'monthly_income': 5000,
            'phone_number': '1234567890',
        }

        response = self.client.post('/api/register/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Customer.objects.count(), 0)
