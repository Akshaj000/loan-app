from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from customer.models import Customer
from loan.models import Loan
from loan.serializers import CheckEligibilityRequestSerializer, CheckEligibilityResponseSerializer
from loan.utils.eligibility import calculate_credit_score, check_loan_eligibility


class CheckEligibilityAPITest(APITestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            age=30,
            monthly_income=5000,
            phone_number='1234567890',
        )

    def test_check_eligibility(self):
        data = {
            'customer_id': self.customer.id,
            'loan_amount': 10000,
            'interest_rate': 10,
            'tenure': 12,
        }

        url = reverse('check_eligibility')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_response_data = {
            'customer_id': self.customer.id,
            'approval': True,
            'interest_rate': 10,
            'corrected_interest_rate': None,
            'tenure': 12,
            'monthly_installment': 876.40,
        }
        self.assertEqual(response.data, expected_response_data)

    def test_invalid_data(self):
        invalid_data = {
            'loan_amount': 10000,
            'interest_rate': 10,
            'tenure': 12,
        }

        url = reverse('check_eligibility')
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('customer_id', response.data)
