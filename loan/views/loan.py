from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from loan.models import Loan
from customer.models import Customer
from loan.serializers import (
    CreateLoanRequestSerializer,
    CreateLoanResponseSerializer,
    ViewLoanResponseSerializer,
    ViewLoansResponseSerializer
)
from loan.utils import check_loan_eligibility
from django.utils import timezone


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def view_loan(request, loan_id: int) -> Response:
    try:
        loan = Loan.objects.get(loan_id=loan_id)
    except Loan.DoesNotExist:
        return Response({'error': 'Loan not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ViewLoanResponseSerializer(loan)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def view_loans(request, customer_id: int) -> Response:
    try:
        loans = Loan.objects.filter(customer__customer_id=customer_id)
    except Loan.DoesNotExist:
        return Response({'error': 'No loans found for the customer.'}, status=status.HTTP_404_NOT_FOUND)

    loan_items = []

    for loan in loans:
        loan_data = {
            'loan_id': loan.loan_id,
            'loan_approved': loan.start_date is not None,
            'loan_amount': loan.loan_amount,
            'interest_rate': loan.interest_rate,
            'monthly_installment': loan.emi,
            'emis_left': loan.emis_left,
        }
        loan_items.append(loan_data)

    serializer = ViewLoansResponseSerializer({'loans': loan_items})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create_loan(request) -> Response:
    if request.method == 'POST':
        serializer = CreateLoanRequestSerializer(data=request.data)
        if serializer.is_valid():
            customer_id = serializer.validated_data['customer_id']
            loan_amount = serializer.validated_data['loan_amount']
            interest_rate = serializer.validated_data['interest_rate']
            tenure = serializer.validated_data['tenure']

            try:
                customer = Customer.objects.get(customer_id=customer_id)
            except Customer.DoesNotExist:
                return Response({'error': 'Customer not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            loans = Loan.objects.filter(customer=customer)
            approval, corrected_interest_rate, monthly_installment = check_loan_eligibility(
                customer.credit_score, loan_amount, interest_rate, tenure, customer.monthly_income, loans
            )
                        
            
            if approval:
                loan = Loan.objects.create(
                    customer=customer,
                    loan_amount=loan_amount,
                    interest_rate=corrected_interest_rate or interest_rate,
                    tenure=tenure,
                    emi=monthly_installment,
                    start_date=timezone.now(),
                )

                response_data = {
                    'loan_id': loan.loan_id,
                    'customer_id': customer_id,
                    'loan_approved': True,
                    'message': 'Loan approved successfully.',
                    'monthly_installment': round(monthly_installment, 2) if monthly_installment else None,
                }
            else:
                response_data = {
                    'loan_id': None,
                    'customer_id': customer_id,
                    'loan_approved': False,
                    'message': 'Loan not approved. Check eligibility criteria.',
                    'monthly_installment': None,
                }

            response_serializer = CreateLoanResponseSerializer(data=response_data)
            if response_serializer.is_valid():
                return Response(response_serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


__all__ = [
    'view_loan',
    'view_loans',
    'create_loan'
]
