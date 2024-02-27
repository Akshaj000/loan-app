from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from customer.views import register_customer   
from loan.views import check_eligibility, create_loan, view_loans, view_loan


urlpatterns = [
    path('api/admin/', admin.site.urls),

    # Customer
    path('api/register/', register_customer),
    
    # loan
    path('api/check-eligibility/', check_eligibility),
    path('api/create-loan/', create_loan),
    path('api/view-loans/<int:customer_id>/', view_loans),
    path('api/view-loan/<int:loan_id>/', view_loan),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
