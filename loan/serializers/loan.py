from rest_framework import serializers


from rest_framework import serializers

class ViewLoanResponseSerializer(serializers.Serializer):
    loan_id = serializers.IntegerField()
    customer = serializers.SerializerMethodField()
    loan_approved = serializers.SerializerMethodField()
    loan_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    monthly_installment = serializers.DecimalField(source='emi', max_digits=10, decimal_places=2)
    tenure = serializers.IntegerField()

    def get_customer(self, loan):
        return {
            'id': loan.customer.customer_id,
            'first_name': loan.customer.first_name,
            'last_name': loan.customer.last_name,
            'phone_number': loan.customer.phone_number,
            'age': loan.customer.age,
        }

    def get_loan_approved(self, loan):
        return loan.start_date is not None




class ViewLoansResponseSerializer(serializers.Serializer):
    loans = serializers.ListField(child=serializers.DictField())

        
class CreateLoanRequestSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()


class CreateLoanResponseSerializer(serializers.Serializer):
    loan_id = serializers.IntegerField(allow_null=True)
    customer_id = serializers.IntegerField()
    loan_approved = serializers.BooleanField()
    message = serializers.CharField()
    monthly_installment = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)


__all__=[
    'ViewLoanResponseSerializer',
    'ViewLoansResponseSerializer',
    'CreateLoanRequestSerializer',
    'CreateLoanResponseSerializer'
]