from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from typing import Dict, Union
from loan.models import Loan
from loan.serializers import CheckEligibilityRequestSerializer, CheckEligibilityResponseSerializer
from customer.models import Customer
from loan.utils.eligibility import check_loan_eligibility, calculate_credit_score


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def check_eligibility(request) -> Response:
    """
    API endpoint to check eligibility for a loan.

    Parameters:
    - request (Dict[str, Union[int, float]]): Request data.

    Returns:
    - Response: JSON response with loan eligibility details.
    """
    if request.method == 'POST':
        serializer = CheckEligibilityRequestSerializer(data=request.data)
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

            credit_score = calculate_credit_score(loans, customer.approved_limit)
            print(credit_score)

            approval, corrected_interest_rate, monthly_installment = check_loan_eligibility(
                credit_score, 
                loan_amount, 
                interest_rate,
                tenure, 
                customer.monthly_income,
                loans
            )

            response_data = {
                'customer_id': customer_id,
                'approval': approval,
                'interest_rate': round(interest_rate, 2) if interest_rate else None,
                'corrected_interest_rate': round(corrected_interest_rate, 2) if corrected_interest_rate else None,
                'tenure': tenure,
                'monthly_installment': round(monthly_installment, 2) if monthly_installment else None,
            }
                        
            response_serializer = CheckEligibilityResponseSerializer(data=response_data)
            if response_serializer.is_valid():
                return Response(response_serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


__all__ = [
    'check_eligibility'
]
