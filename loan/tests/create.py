from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from customer.models import Customer
from loan.serializers import CreateLoanResponseSerializer
from loan.utils.eligibility import check_loan_eligibility
from django.utils import timezone

class CreateLoanAPITest(APITestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            age=30,
            monthly_income=5000,
            phone_number='1234567890',
        )

    def test_create_loan(self):
        data = {
            'customer_id': self.customer.customer_id,
            'loan_amount': 10000,
            'interest_rate': 10,
            'tenure': 12,
        }
        response = self.client.post('/api/create-loan/', data, format='json')
        print(response)
        assert response.status_code == status.HTTP_201_CREATED
        expected_response_data = CreateLoanResponseSerializer(response.data).data
        assert response.data == expected_response_data

    def test_create_loan_customer_not_found(self):
        invalid_data = {
            'customer_id': 999,
            'loan_amount': 10000,
            'interest_rate': 10,
            'tenure': 12,
        }
        response = self.client.post('/api/create-loan/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
