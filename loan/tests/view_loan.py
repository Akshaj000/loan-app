from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from customer.models import Customer
from loan.models import Loan
from loan.serializers import ViewLoanResponseSerializer
from django.utils import timezone


class ViewLoanAPITest(APITestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            age=30,
            monthly_income=5000,
            phone_number='1234567890',
        )
        self.loan = Loan.objects.create(
            customer=self.customer,
            loan_amount=10000,
            interest_rate=10,
            tenure=12,
            emi=876.40,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=365),
            loan_approved=True,
        )

    def test_view_loan(self):
        url = reverse('view_loan', args=[self.loan.loan_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response_data = ViewLoanResponseSerializer(self.loan).data
        self.assertEqual(response.data, expected_response_data)

    def test_view_loan_not_found(self):
        url = reverse('view_loan', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
