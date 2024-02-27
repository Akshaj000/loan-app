from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from customer.models import Customer
from loan.models import Loan
from loan.serializers import ViewLoanResponseSerializer, ViewLoansResponseSerializer
from django.utils import timezone


class ViewLoansAPITest(APITestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            age=30,
            monthly_income=5000,
            phone_number='1234567890',
        )
        self.loan1 = Loan.objects.create(
            customer=self.customer,
            loan_amount=10000,
            interest_rate=10,
            tenure=12,
            emi=876.40,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=365),  # Assuming a 1-year loan
            loan_approved=True,
        )
        self.loan2 = Loan.objects.create(
            customer=self.customer,
            loan_amount=15000,
            interest_rate=12,
            tenure=18,
            emi=1200.50,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=547),
            loan_approved=False,
        )

    def test_view_loans(self):
        url = reverse('view_loans', args=[self.customer.customer_id]) 
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_response_data = ViewLoansResponseSerializer({'loans': [
            ViewLoanResponseSerializer(self.loan1).data,
            ViewLoanResponseSerializer(self.loan2).data,
        ]}).data
        self.assertEqual(response.data, expected_response_data)

    def test_view_loans_no_loans_found(self):
        url = reverse('view_loans', args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

