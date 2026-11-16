import csv # Create and write CSV files
import random # Generate simulated invoice data
from datetime import date, timedelta # date: Work with invoice dates
# timedelta: Calculate due dates and payment delays
from pathlib import Path # Locate project folders and files

# Project configuration
TOTAL_INVOICES = 500 # We want to generate 500 invoice records.
RANDOM_SEED = 99 # Keeps random selections consistent across executions.
random.seed(RANDOM_SEED) # Initializes the random generator.

# Dataset date boundaries
START_DATE = date(2025, 1, 1) # Earliest possible invoice date.

# Our fixed reporting date for calculating overdue and pending invoices.
AS_OF_DATE = date(2026, 11, 11) 

# Why use a fixed reporting date?
# Suppose you run this script today and again next month. 
# If the reporting date changes automatically, 
# some invoices might change from Pending to Overdue.

# Invoice payment terms
PAYMENT_TERMS = [
    "Net 15", # Net 15 means payment is due within 15 days.
    "Net 30",
    "Net 45",
    "Net 60"
]

# Available invoice payment statuses
PAYMENT_STATUSES = [
    "Paid", # The invoice has been paid.
    "Pending", # Payment is not yet completed, but the due date has not passed.
    "Overdue" # Payment is not completed and the due date has passed.
]

# Available payment methods
PAYMENT_METHODS = [
    "NEFT", # National Electronic Funds Transfer
    "RTGS", # Real Time Gross Settlement
    "IMPS", # Immediate Payment Service
    "UPI", # Unified Payments Interface
    "Cheque" # Paper-based payment
]

# Function to load vendor IDs from vendor master CSV
def load_vendor_ids():
    project_root = Path(__file__).resolve().parents[1]
    vendor_file = project_root / "data" / "raw" / "vendor_master.csv"
    with open(vendor_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        vendor_ids = [row["vendor_id"] for row in reader]

    return vendor_ids

# Function to generate a random invoice date
def generate_invoice_date():
    total_days = (AS_OF_DATE - START_DATE).days
    random_days = random.randint(0, total_days)
    invoice_date = START_DATE + timedelta(days=random_days)

    return invoice_date

# Function to load vendor payment terms
def load_vendor_payment_terms():
    project_root = Path(__file__).resolve().parents[1]
    vendor_file = project_root / "data" / "raw" / "vendor_master.csv"
    with open(vendor_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        vendor_terms = {
            row["vendor_id"]: row["payment_terms"]
            for row in reader
        }

    return vendor_terms


# Function to calculate invoice due date
def calculate_due_date(invoice_date, payment_terms):

    payment_days = int(payment_terms.split()[1]) # separates "Net 30" into ["Net", "30"]
    # [1] extracts 30
    # int() converts it into a number
    due_date = invoice_date + timedelta(days=payment_days)
    # timedelta() adds those days to the invoice date
    return due_date


# Function to generate one invoice record
def generate_invoice_record(invoice_number, vendor_ids, vendor_terms):
    # Select a vendor
    vendor_id = random.choice(vendor_ids)
    # Retrieve the vendor's payment terms
    payment_terms = vendor_terms[vendor_id]
    # Generate invoice date
    invoice_date = generate_invoice_date()
    # Calculate invoice due date
    due_date = calculate_due_date(invoice_date, payment_terms)
    # Generate invoice amount between ₹5,000 and ₹2,50,000
    invoice_amount = round(random.uniform(5000, 250000), 2)
    # Create invoice record
    invoice_record = {
        "invoice_id": f"INV-{invoice_number:04d}",
        "vendor_id": vendor_id,
        "invoice_date": invoice_date,
        "due_date": due_date,
        "payment_terms": payment_terms,
        "invoice_amount": invoice_amount
    }

    return invoice_record



# Main function to generate all invoice transactions
def main():
    # Load vendor information
    vendor_ids = load_vendor_ids()
    vendor_terms = load_vendor_payment_terms()
    # Create an empty list to store invoice records
    invoice_records = []
    # Generate 500 invoice records
    for invoice_number in range(1, TOTAL_INVOICES + 1):
        invoice = generate_invoice_record(
            invoice_number,
            vendor_ids,
            vendor_terms
        )
        invoice_records.append(invoice)

    # Define output file location
    project_root = Path(__file__).resolve().parents[1]
    output_file = (
        project_root
        / "data"
        / "processed"
        / "invoice_transactions.csv"
    )

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Write invoice records into CSV
    with open(output_file, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=invoice_records[0].keys()
        )

        writer.writeheader()
        writer.writerows(invoice_records)

    print("Successfully generated invoice transactions!")
    print("Total invoices:", len(invoice_records))
    print("Output file:", output_file)


# Execute main function
if __name__ == "__main__":
    main()