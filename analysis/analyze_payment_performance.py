
# Import required libraries
import csv
from pathlib import Path
from datetime import datetime


# --------------------------------------------------
# 1. DEFINE PROJECT PATHS
# --------------------------------------------------

# Get the root directory of the project
project_root = Path(__file__).resolve().parents[1]

# Define the invoice dataset path
invoice_file = (
    project_root
    / "data"
    / "processed"
    / "invoice_transactions.csv"
)

# Define the payment register path
payment_file = (
    project_root
    / "data"
    / "processed"
    / "payment_register.csv"
)


# --------------------------------------------------
# 2. DEFINE REPORTING DATE
# --------------------------------------------------

# Use the same reporting date used during payment generation
reporting_date = datetime.strptime(
    "2026-11-11", "%Y-%m-%d"
).date()


# --------------------------------------------------
# 3. CREATE A FUNCTION TO LOAD CSV FILES
# --------------------------------------------------

def load_csv(file_path):

    # Open the CSV file in read mode
    with open(file_path, "r", newline="", encoding="utf-8") as file:

        # Read CSV rows as dictionaries
        reader = csv.DictReader(file)

        # Store all records in a list
        records = list(reader)

    # Return the loaded records
    return records


# --------------------------------------------------
# 4. MAIN FUNCTION
# --------------------------------------------------

def main():

    # Load invoice and payment records
    invoices = load_csv(invoice_file)
    payments = load_csv(payment_file)

    print("VENDOR PAYMENT PERFORMANCE ANALYSIS")
    print("-----------------------------------")

    # --------------------------------------------------
    # 5. MATCH INVOICES WITH PAYMENT RECORDS
    # --------------------------------------------------

    # Create a dictionary using invoice_id as the key
    # This allows us to quickly find payment details for an invoice
    payment_lookup = {
        row["invoice_id"]: row for row in payments
    }

    # Initialize financial and performance metrics
    total_invoice_value = 0
    total_paid_amount = 0
    total_outstanding_amount = 0
    total_overdue_amount = 0

    paid_count = 0
    overdue_count = 0
    pending_count = 0

    total_overdue_days = 0

    # Count invoices without a matching payment record
    unmatched_invoices = 0

    # --------------------------------------------------
    # 6. ANALYZE EACH INVOICE
    # --------------------------------------------------

    for invoice in invoices:

        # Extract invoice details
        invoice_id = invoice["invoice_id"]
        invoice_amount = float(invoice["invoice_amount"])

        # Find the matching payment record
        payment = payment_lookup.get(invoice_id)

        # Skip invoices without a matching payment record
        if payment is None:
            unmatched_invoices += 1
            continue

        # Extract payment status
        payment_status = payment["payment_status"]

        # Add invoice amount to total invoice value
        total_invoice_value += invoice_amount

        # Calculate metrics based on payment status
        if payment_status == "Paid":

            # Add paid invoice amount
            total_paid_amount += invoice_amount
            paid_count += 1

        elif payment_status == "Overdue":

            # Add overdue invoice amount to outstanding value
            total_outstanding_amount += invoice_amount
            total_overdue_amount += invoice_amount

            overdue_count += 1

            # Calculate how many days the invoice is overdue
            due_date = datetime.strptime(
                payment["due_date"], "%Y-%m-%d"
            ).date()

            overdue_days = (reporting_date - due_date).days

            total_overdue_days += overdue_days

        elif payment_status == "Pending":

            # Add pending invoice amount to outstanding value
            total_outstanding_amount += invoice_amount
            pending_count += 1

    # --------------------------------------------------
    # 7. CALCULATE PERFORMANCE INDICATORS
    # --------------------------------------------------

    # Calculate payment completion rate by invoice count
    if len(invoices) > 0:

        payment_completion_rate = (
            paid_count / len(invoices)
        ) * 100

    else:
        payment_completion_rate = 0

    # Calculate average overdue days
    if overdue_count > 0:

        average_overdue_days = (
            total_overdue_days / overdue_count
        )

    else:
        average_overdue_days = 0

    # Calculate outstanding percentage of invoice value
    if total_invoice_value > 0:

        outstanding_percentage = (
            total_outstanding_amount / total_invoice_value
        ) * 100

    else:
        outstanding_percentage = 0

    # --------------------------------------------------
    # 8. DISPLAY FINANCIAL SUMMARY
    # --------------------------------------------------

    print("\nFINANCIAL SUMMARY")
    print("-----------------")

    print(f"Total invoice value: Rs. {total_invoice_value:,.2f}")
    print(f"Total paid amount: Rs. {total_paid_amount:,.2f}")
    print(f"Total outstanding amount: Rs. {total_outstanding_amount:,.2f}")
    print(f"Total overdue amount: Rs. {total_overdue_amount:,.2f}")

    # --------------------------------------------------
    # 9. DISPLAY PAYMENT PERFORMANCE
    # --------------------------------------------------

    print("\nPAYMENT PERFORMANCE")
    print("-------------------")

    print("Total invoices:", len(invoices))
    print("Paid invoices:", paid_count)
    print("Overdue invoices:", overdue_count)
    print("Pending invoices:", pending_count)

    print(
        f"Payment completion rate: "
        f"{payment_completion_rate:.2f}%"
    )

    print(
        f"Outstanding percentage: "
        f"{outstanding_percentage:.2f}%"
    )

    print(
        f"Average overdue days: "
        f"{average_overdue_days:.2f}"
    )

    print("Unmatched invoices:", unmatched_invoices)


# --------------------------------------------------
# 10. EXECUTE THE MAIN FUNCTION
# --------------------------------------------------

# Run the main function when this script is executed directly
if __name__ == "__main__":
    main()
