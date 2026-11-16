
# Import required libraries
import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime


# --------------------------------------------------
# 1. DEFINE PROJECT PATHS
# --------------------------------------------------

# Get the root directory of the project
project_root = Path(__file__).resolve().parents[1]

# Define input dataset paths
invoice_file = (
    project_root / "data" / "processed" / "invoice_transactions.csv"
)

payment_file = (
    project_root / "data" / "processed" / "payment_register.csv"
)

# Define output folder
reports_folder = project_root / "reports"

# Create the reports folder if it does not exist
reports_folder.mkdir(parents=True, exist_ok=True)

# Define output CSV paths
kpi_file = reports_folder / "dashboard_kpis.csv"
status_file = reports_folder / "payment_status_summary.csv"


# --------------------------------------------------
# 2. DEFINE REPORTING DATE
# --------------------------------------------------

# Use the same reporting date as the payment register
reporting_date = datetime.strptime(
    "2026-11-11", "%Y-%m-%d"
).date()


# --------------------------------------------------
# 3. CREATE A CSV LOADING FUNCTION
# --------------------------------------------------

def load_csv(file_path):

    # Open the CSV file in read mode
    with open(file_path, "r", newline="", encoding="utf-8") as file:

        # Read CSV rows as dictionaries
        reader = csv.DictReader(file)

        # Store all rows in a list
        records = list(reader)

    return records


# --------------------------------------------------
# 4. CREATE A CSV EXPORT FUNCTION
# --------------------------------------------------

def export_csv(file_path, fieldnames, records):

    # Open the output CSV file in write mode
    with open(file_path, "w", newline="", encoding="utf-8") as file:

        # Create a CSV writer using dictionary records
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write column headers
        writer.writeheader()

        # Write all data records
        writer.writerows(records)


# --------------------------------------------------
# 5. MAIN FUNCTION
# --------------------------------------------------

def main():

    # Load invoice and payment datasets
    invoices = load_csv(invoice_file)
    payments = load_csv(payment_file)

    # Match payment records using invoice ID
    payment_lookup = {
        row["invoice_id"]: row for row in payments
    }

    # Initialize financial metrics
    total_invoice_value = 0
    total_paid_amount = 0
    total_outstanding_amount = 0
    total_overdue_amount = 0

    # Initialize invoice counts
    paid_count = 0
    overdue_count = 0
    pending_count = 0
    unmatched_count = 0

    # Initialize overdue-day calculation
    total_overdue_days = 0

    # Store status-wise invoice count and value
    status_summary = defaultdict(
        lambda: {"invoice_count": 0, "invoice_value": 0}
    )

    # --------------------------------------------------
    # 6. PROCESS EACH INVOICE
    # --------------------------------------------------

    for invoice in invoices:

        # Extract invoice details
        invoice_id = invoice["invoice_id"]
        invoice_amount = float(invoice["invoice_amount"])

        # Find corresponding payment record
        payment = payment_lookup.get(invoice_id)

        # Count invoices without a payment record
        if payment is None:
            unmatched_count += 1
            continue

        # Extract payment status
        status = payment["payment_status"]

        # Add invoice value to total invoice value
        total_invoice_value += invoice_amount

        # Update status-wise count and value
        status_summary[status]["invoice_count"] += 1
        status_summary[status]["invoice_value"] += invoice_amount

        # Calculate metrics for paid invoices
        if status == "Paid":

            paid_count += 1
            total_paid_amount += invoice_amount

        # Calculate metrics for overdue invoices
        elif status == "Overdue":

            overdue_count += 1
            total_outstanding_amount += invoice_amount
            total_overdue_amount += invoice_amount

            # Calculate overdue days
            due_date = datetime.strptime(
                payment["due_date"], "%Y-%m-%d"
            ).date()

            total_overdue_days += (
                reporting_date - due_date
            ).days

        # Calculate metrics for pending invoices
        elif status == "Pending":

            pending_count += 1
            total_outstanding_amount += invoice_amount

    # --------------------------------------------------
    # 7. CALCULATE KPI METRICS
    # --------------------------------------------------

    total_invoices = len(invoices)

    # Calculate payment completion rate by invoice count
    payment_completion_rate = (
        paid_count / total_invoices * 100
        if total_invoices else 0
    )

    # Calculate outstanding percentage by invoice value
    outstanding_percentage = (
        total_outstanding_amount / total_invoice_value * 100
        if total_invoice_value else 0
    )

    # Calculate average overdue days
    average_overdue_days = (
        total_overdue_days / overdue_count
        if overdue_count else 0
    )

    # --------------------------------------------------
    # 8. PREPARE KPI SUMMARY
    # --------------------------------------------------

    # Store KPI names and their calculated values
    kpi_records = [
        {"metric": "Total Invoices", "value": total_invoices},
        {"metric": "Total Invoice Value", "value": round(total_invoice_value, 2)},
        {"metric": "Paid Invoices", "value": paid_count},
        {"metric": "Paid Amount", "value": round(total_paid_amount, 2)},
        {"metric": "Overdue Invoices", "value": overdue_count},
        {"metric": "Overdue Amount", "value": round(total_overdue_amount, 2)},
        {"metric": "Pending Invoices", "value": pending_count},
        {"metric": "Outstanding Amount", "value": round(total_outstanding_amount, 2)},
        {"metric": "Payment Completion Rate (%)", "value": round(payment_completion_rate, 2)},
        {"metric": "Outstanding Percentage (%)", "value": round(outstanding_percentage, 2)},
        {"metric": "Average Overdue Days", "value": round(average_overdue_days, 2)},
        {"metric": "Unmatched Invoices", "value": unmatched_count}
    ]

    # --------------------------------------------------
    # 9. PREPARE PAYMENT STATUS SUMMARY
    # --------------------------------------------------

    # Define a consistent order for payment statuses
    statuses = ["Paid", "Overdue", "Pending"]

    # Create one summary row for each status
    status_records = []

    for status in statuses:

        status_records.append({
            "payment_status": status,
            "invoice_count": status_summary[status]["invoice_count"],
            "invoice_value": round(
                status_summary[status]["invoice_value"], 2
            )
        })

    # --------------------------------------------------
    # 10. EXPORT DASHBOARD CSV FILES
    # --------------------------------------------------

    # Export financial and performance KPIs
    export_csv(
        kpi_file,
        ["metric", "value"],
        kpi_records
    )

    # Export payment status summary
    export_csv(
        status_file,
        ["payment_status", "invoice_count", "invoice_value"],
        status_records
    )

    # Display export results
    print("DASHBOARD DATA EXPORT")
    print("---------------------")
    print("Total invoices processed:", total_invoices)
    print("Unmatched invoices:", unmatched_count)
    print("KPI file:", kpi_file)
    print("Status summary file:", status_file)
    print("Dashboard data exported successfully!")


# --------------------------------------------------
# 11. EXECUTE MAIN FUNCTION
# --------------------------------------------------

if __name__ == "__main__":
    main()
