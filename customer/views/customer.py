from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from typing import Dict, Any, Union
from customer.models import Customer
from customer.serializers import (
    CustomerRegisterRequestBodySerializer, 
    CustomerRegisterResponseBodySerializer
)
from customer.models.customer import Customer


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register_customer(request) -> Response:
    if request.method == 'POST':
        serializer = CustomerRegisterRequestBodySerializer(data=request.data)
        if serializer.is_valid():        
            customer: Customer = Customer.objects.create(**serializer.validated_data)

            response_data: Dict[str, Any] = {
                'customer_id': customer.customer_id,
                'name': f"{customer.first_name} {customer.last_name}",
                'age': customer.age,
                'monthly_income': customer.monthly_income,
                'approved_limit': customer.approved_limit,
                'phone_number': customer.phone_number
            }

            response_serializer = CustomerRegisterResponseBodySerializer(data=response_data)
            if response_serializer.is_valid():
                return Response(response_serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


__all__ = ['register_customer']
