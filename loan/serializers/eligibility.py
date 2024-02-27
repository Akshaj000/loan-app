from rest_framework import serializers

class CheckEligibilityRequestSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()


class CheckEligibilityResponseSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    approval = serializers.BooleanField()
    interest_rate = serializers.DecimalField(decimal_places=2, max_digits=5)
    corrected_interest_rate = serializers.DecimalField(allow_null=True, decimal_places=2, max_digits=5)
    tenure = serializers.IntegerField()
    monthly_installment = serializers.DecimalField(allow_null=True, decimal_places=2, max_digits=10)


__all__=[
    'CheckEligibilityRequestSerializer',
    'CheckEligibilityResponseSerializer'
]
