from typing import Dict, List, Optional, Tuple, Union
from loan.models import Loan

def calculate_credit_score(loans: List[Loan], approved_limit: float) -> float:
    """
    Calculate credit score based on historical loan data.

    Parameters:
    - loans (List[Loan]): List of Loan objects.
    - approved_limit (float): Approved credit limit.

    Returns:
    - float: Calculated credit score.
    """
    on_time_payments = sum(1 for loan in loans if loan.emis_paid_on_time > 0)
    num_loans_taken = len(loans)
    loan_activity_current_year = sum(1 for loan in loans if loan.start_date.year == 2024)
    loan_approved_volume = sum(loan.loan_amount for loan in loans)

    if sum(loan.emi for loan in loans) > approved_limit:
        credit_score = 0
    else:
        on_time_payments_normalized = min((on_time_payments / num_loans_taken) * 100, 100)
        loan_activity_normalized = min((loan_activity_current_year / num_loans_taken) * 100, 100)
        loan_approved_volume_normalized = min((loan_approved_volume / approved_limit) * 100, 50)

        credit_score = (
            on_time_payments_normalized * 0.35 +
            num_loans_taken * 0.30 +
            loan_activity_normalized * 0.15 +
            loan_approved_volume_normalized * 0.20
        )
    return credit_score

def check_loan_eligibility(
    credit_score: float, 
    loan_amount: float, 
    interest_rate: float, 
    tenure: int, 
    monthly_salary: float,
    loans: List[Loan]
) -> Tuple[bool, Optional[float], Optional[float]]:
    """
    Check loan eligibility based on credit score and other criteria.

    Parameters:
    - credit_score (float): Credit score of the customer.
    - loan_amount (float): Requested loan amount.
    - interest_rate (float): Interest rate on the loan.
    - tenure (int): Tenure of the loan.
    - monthly_salary (float): Monthly salary of the customer.

    Returns:
    - Tuple[bool, Optional[float], Optional[float]]: A tuple containing
      approval status, corrected interest rate, and monthly installment.
    """
    if credit_score > 50:
        approval = True
        interest_rate = None
    elif 30 < credit_score <= 50:
        approval = interest_rate > 12
        interest_rate = 12 if not approval else interest_rate
    elif 10 < credit_score <= 30:
        approval = interest_rate > 16
        interest_rate = 16 if not approval else interest_rate
    else:
        approval = False
        interest_rate = None
    
    if (sum(loan.emi for loan in loans) > 0.5 * monthly_salary):
        approval = False
    
    
    monthly_installment = (
        loan_amount * (interest_rate / 100) / 12 /
        (1 - (1 + (interest_rate / 100) / 12) ** (-tenure))
    ) if approval else None
        
    return approval, interest_rate, monthly_installment

__all__ = [
    'calculate_credit_score',
    'check_loan_eligibility'
]
