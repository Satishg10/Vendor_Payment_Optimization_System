# Import required libraries
import csv
from pathlib import Path
from collections import Counter
from datetime import datetime


# --------------------------------------------------
# 1. DEFINE PROJECT FILE PATHS
# --------------------------------------------------

# Get the root directory of the project
project_root = Path(__file__).resolve().parents[1]

# Define the location of the generated payment register
payment_file = (
    project_root
    / "data"
    / "processed"
    / "payment_register.csv"
)


# --------------------------------------------------
# 2. CREATE A FUNCTION TO LOAD CSV DATA
# --------------------------------------------------

def load_csv(file_path):

    # Open the CSV file in read mode
    with open(file_path, "r", newline="", encoding="utf-8") as file:

        # DictReader reads each CSV row as a dictionary
        reader = csv.DictReader(file)

        # Convert all rows into a list
        records = list(reader)

    # Return the list of records
    return records


# --------------------------------------------------
# 3. MAIN FUNCTION
# --------------------------------------------------

def main():

    # Load payment records from the CSV file
    payments = load_csv(payment_file)

    print("PAYMENT REGISTER VALIDATION")
    print("---------------------------")

    # --------------------------------------------------
    # CHECK 1: TOTAL NUMBER OF PAYMENT RECORDS
    # --------------------------------------------------

    # Count the total number of payment records
    total_records = len(payments)

    print("Total payment records:", total_records)

    # --------------------------------------------------
    # CHECK 2: DUPLICATE INVOICE IDs
    # --------------------------------------------------

    # Extract all invoice IDs into a list
    invoice_ids = [row["invoice_id"] for row in payments]

    # Compare total IDs with unique IDs to find duplicates
    duplicate_ids = len(invoice_ids) - len(set(invoice_ids))

    print("Duplicate invoice IDs:", duplicate_ids)

    # --------------------------------------------------
    # CHECK 3: MISSING REQUIRED VALUES
    # --------------------------------------------------

    # Define columns that must contain values
    required_fields = [
        "invoice_id",
        "vendor_id",
        "due_date",
        "payment_amount",
        "payment_status"
    ]

    # Start the missing-value counter at zero
    missing_values = 0

    # Check every record and every required field
    for row in payments:

        for field in required_fields:

            # Count fields containing empty values
            if row[field].strip() == "":
                missing_values += 1

    print("Missing required values:", missing_values)

    # --------------------------------------------------
    # CHECK 4: INVALID PAYMENT STATUSES
    # --------------------------------------------------

    # Define the only payment statuses allowed
    valid_statuses = {"Paid", "Overdue", "Pending"}

    # Collect records containing an invalid status
    invalid_statuses = [
        row for row in payments
        if row["payment_status"] not in valid_statuses
    ]

    print("Invalid payment statuses:", len(invalid_statuses))

    # --------------------------------------------------
    # CHECK 5: VALIDATE PAID AND UNPAID RECORDS
    # --------------------------------------------------

    # Initialize counters for incorrect payment records
    invalid_paid_records = 0
    invalid_unpaid_records = 0

    # Examine each payment record
    for row in payments:

        # Extract the payment details
        status = row["payment_status"]
        amount = float(row["payment_amount"])
        payment_date = row["payment_date"]

        # A Paid record must have a positive amount and valid date
        if status == "Paid":

            if amount <= 0 or payment_date == "":
                invalid_paid_records += 1

            else:
                try:
                    # Check whether the payment date follows YYYY-MM-DD
                    datetime.strptime(payment_date, "%Y-%m-%d")

                except ValueError:
                    # Count dates that do not match the expected format
                    invalid_paid_records += 1

        # Overdue and Pending records must not show a payment
        elif status in {"Overdue", "Pending"}:

            if amount != 0 or payment_date != "":
                invalid_unpaid_records += 1

    print("Invalid paid records:", invalid_paid_records)
    print("Invalid unpaid records:", invalid_unpaid_records)

    # --------------------------------------------------
    # CHECK 6: PAYMENT STATUS DISTRIBUTION
    # --------------------------------------------------

    # Count how many records belong to each payment status
    status_counts = Counter(
        row["payment_status"] for row in payments
    )

    print("\nPAYMENT STATUS DISTRIBUTION")

    # Display the count for each status
    for status, count in status_counts.items():

        print(f"{status}: {count}")

    # --------------------------------------------------
    # CHECK 7: FINAL VALIDATION RESULT
    # --------------------------------------------------

    # Validation passes only if all defined checks are successful
    if (
        total_records == 500
        and duplicate_ids == 0
        and missing_values == 0
        and len(invalid_statuses) == 0
        and invalid_paid_records == 0
        and invalid_unpaid_records == 0
    ):

        print("\nVALIDATION PASSED")

    else:

        print("\nVALIDATION FAILED")


# --------------------------------------------------
# 4. EXECUTE THE MAIN FUNCTION
# --------------------------------------------------

# Run main() only when this file is executed directly
if __name__ == "__main__":
    main()
