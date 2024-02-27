## A basic django rest endpoint with celery task to initialize the database using the excel sheets.

### /register

- Add a new customer to the customer table with an approved limit based on salary.
  - `approved_limit = 36 * monthly_salary` (rounded to the nearest lakh).
- **Request Body:**
  - `first_name` (string): First Name of customer
  - `last_name` (string): Last Name of customer
  - `age` (int): Age of customer
  - `monthly_income` (int): Monthly income of the individual
  - `phone_number` (int): Phone number of the customer
- **Response Body:**
  - `customer_id` (int): ID of the customer
  - `name` (string): Name of the customer
  - `age` (int): Age of the customer
  - `monthly_income` (int): Monthly income of the individual
  - `approved_limit` (int): Approved credit limit
  - `phone_number` (int): Phone number of the customer

### /check-eligibility

- Check loan eligibility based on the credit score of the customer.
- Assign a credit score based on historical loan data.
- Approve loans based on credit score and other criteria.
- **Request Body:**
  - `customer_id` (int): ID of the customer
  - `loan_amount` (float): Requested loan amount
  - `interest_rate` (float): Interest rate on the loan
  - `tenure` (int): Tenure of the loan
- **Response Body:**
  - `customer_id` (int): ID of the customer
  - `approval` (bool): Can the loan be approved
  - `interest_rate` (float): Interest rate on the loan
  - `corrected_interest_rate` (float): Corrected interest rate based on credit rating (if applicable)
  - `tenure` (int): Tenure of the loan
  - `monthly_installment` (float): Monthly installment to be paid as repayment

### /create-loan

- Process a new loan based on eligibility.
- **Request Body:**
  - `customer_id` (int): ID of the customer
  - `loan_amount` (float): Requested loan amount
  - `interest_rate` (float): Interest rate on the loan
  - `tenure` (int): Tenure of the loan
- **Response Body:**
  - `loan_id` (int): ID of the approved loan (null otherwise)
  - `customer_id` (int): ID of the customer
  - `loan_approved` (bool): Is the loan approved
  - `message` (string): Appropriate message if the loan is not approved
  - `monthly_installment` (float): Monthly installment to be paid as repayment

### /view-loan/{loan_id}

- View loan details and customer details.
- **Response Body:**
  - `loan_id` (int): ID of the approved loan
  - `customer` (JSON): JSON containing customer details (id, first_name, last_name, phone_number, age)
  - `loan_approved` (bool): Is the loan approved
  - `loan_amount` (float): Loan amount
  - `interest_rate` (float): Interest rate of the approved loan
  - `monthly_installment` (float): Monthly installment to be paid as repayment
  - `tenure` (int): Tenure of the loan

### /view-loans/{customer_id}

- View all current loan details by customer ID.
- **Response Body (List of loan items):**
  - `loan_id` (int): ID of the approved loan
  - `loan_approved` (bool): Is the loan approved
  - `interest_rate` (float): Interest rate of the approved loan
  - `monthly_installment` (float): Monthly installment to be paid as repayment
  - `repayments_left` (int): Number of EMIs left