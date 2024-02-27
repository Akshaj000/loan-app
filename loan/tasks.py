import pandas as pd
from customer.models import Customer
from loan.models import Loan
from datetime import datetime, timezone
import celery

def convert_date_to_timestamp(date_input):
    date_format = "%m/%d/%Y"

    if isinstance(date_input, pd.Timestamp):
        date_str = date_input.strftime(date_format)
    else:
        date_str = date_input

    try:
        date_obj = datetime.strptime(date_str, date_format)
        timestamp = date_obj.replace(tzinfo=timezone.utc).timestamp()
        return int(timestamp)
    except ValueError:
        print(f"Error: Invalid date format - {date_str}")
        return None


def ingest_customer_data(file_path):
    customer_data = pd.read_excel(file_path)

    for index, row in customer_data.iterrows():
        print(f"Processing row {index + 1} - {row}")

        if not Customer.objects.filter(customer_id=row['Customer ID']).exists():
            print(f"Creating customer: {row['First Name']} {row['Last Name']} (ID: {row['Customer ID']})")
            Customer.objects.create(
                customer_id=row['Customer ID'],
                first_name=row['First Name'],
                last_name=row['Last Name'],
                phone_number=row['Phone Number'],
                age=row['Age'],
                monthly_income=row['Monthly Salary'],
                approved_limit=row['Approved Limit'],
            )
            print(f"Customer created successfully!")

    print("Ingestion process completed.")

def ingest_loan_data(file_path):
    loan_data = pd.read_excel(file_path)

    for index, row in loan_data.iterrows():
        print(f"Processing row {index + 1} - {row}")

        if not Loan.objects.filter(loan_id=row['Loan ID']).exists():
            start_date = convert_date_to_timestamp(row['Date of Approval'])
            end_date = convert_date_to_timestamp(row['End Date'])
            print(f"Creating loan: {row['Loan ID']} for customer {row['Customer ID']}")
            Loan.objects.create(
                customer_id=row['Customer ID'],
                loan_id=row['Loan ID'],
                loan_amount=row['Loan Amount'],
                tenure=row['Tenure'],
                interest_rate=row['Interest Rate'],
                emi=row['Monthly payment'],
                emis_paid_on_time=row['EMIs paid on Time'],
                start_date=datetime.utcfromtimestamp(start_date),
                end_date=datetime.utcfromtimestamp(end_date)
            )
            print(f"Loan created successfully!")

    print("Ingestion process completed.")


@celery.shared_task
def ingest_data(file_path=""):
    ingest_customer_data("customer_data.xlsx")
    ingest_loan_data("loan_data.xlsx")