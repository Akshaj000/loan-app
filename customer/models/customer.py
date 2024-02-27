from django.db import models


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    monthly_income = models.IntegerField(default=0)
    current_debt = models.IntegerField(default=0)
    approved_limit = models.IntegerField(null=True, blank=True)
    
    @property
    def credit_score(self):
        from loan.utils import calculate_credit_score
        from loan.models import Loan
        loans = Loan.objects.filter(customer=self)
        return calculate_credit_score(loans, self.approved_limit)
    
    def handle_approved_limit(self):
        return round(36 * self.monthly_income)

    def save(self, *args, **kwargs):
        if self.approved_limit is None:
            self.approved_limit = self.handle_approved_limit()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


__all__ = ['Customer']
