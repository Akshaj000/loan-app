from django.db import models
from customer.models import Customer
from django.utils import timezone

class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_amount = models.FloatField()
    tenure = models.IntegerField()
    interest_rate = models.FloatField()
    emi = models.FloatField()
    emis_paid_on_time = models.IntegerField(default=0)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    
    @property
    def emis_left(self):
        emis_left = self.tenure - self.emis_paid_on_time
        return max(emis_left, 0)
    
    def save(self, *args, **kwargs):
        if self.end_date is None and self.tenure and self.start_date:
            self.end_date = self.start_date + timezone.timedelta(days=self.tenure * 30)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'
    
    def __str__(self):
        return str(self.loan_id)


__all__ = ['Loan']
