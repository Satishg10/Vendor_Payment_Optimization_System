import csv # Read and write CSV files
from pathlib import Path # Handle project folder and file paths
from datetime import datetime, timedelta 
# datetime - Work with payment dates and due dates

project_root = Path(__file__).resolve().parents[1]

invoice_file = ( # Existing dataset from which we'll read invoice records.
    project_root
    / "data"
    / "processed"
    / "invoice_transactions.csv"
)

payment_file = ( # New CSV file that we'll generate
    project_root
    / "data"
    / "processed"
    / "payment_register.csv"
)

def load_csv(file_path): # Defines a function that accepts a file path
  # open() - Opens the CSV file
  # "r" - Opens the file in read mode
    with open(file_path, "r", newline="", encoding="utf-8") as file:
      # csv.DictReader(file) - Reads each CSV row as a dictionary.
        reader = csv.DictReader(file)
        # list(reader) -	Converts all rows into a list
        records = list(reader)

    return records # return records	Returns the collected records
    
def main():
    # Load invoice records
    invoices = load_csv(invoice_file)

    # Define reporting date
    reporting_date = datetime.strptime(
        "2026-11-11", "%Y-%m-%d"
    ).date()

    # datetime.strptime() - converts a date string into a datetime object
    # %Y-%m-%d - specifies the date format.
    # .date() - extracts only the date, without the time.

    # Create an empty list for payment records
    payment_records = []

    # Process each invoice
    for invoice in invoices:

        invoice_id = invoice["invoice_id"]
        vendor_id = invoice["vendor_id"]

        invoice_date = datetime.strptime(
            invoice["invoice_date"], "%Y-%m-%d"
        ).date()

        due_date = datetime.strptime(
            invoice["due_date"], "%Y-%m-%d"
        ).date()

        invoice_amount = float(invoice["invoice_amount"])

        # Determine payment status
        payment_date = ""
        invoice_number = int(invoice_id.split("-")[1])

        if due_date <= reporting_date and invoice_number % 3 == 0:
            payment_status = "Paid"
            payment_date = (
                due_date - timedelta(days=1)
            ).strftime("%Y-%m-%d")

        elif due_date < reporting_date:
            payment_status = "Overdue"

        else:
            payment_status = "Pending"

        # Add payment record to the list
        payment_records.append({
            "invoice_id": invoice_id,
            "vendor_id": vendor_id,
            "due_date": due_date.strftime("%Y-%m-%d"),
            "payment_date": payment_date,
            "payment_amount": (
                invoice_amount if payment_status == "Paid" else 0
            ),
            "payment_status": payment_status
        })

    # Write payment records to CSV
    with open(payment_file, "w", newline="", encoding="utf-8") as file:

        fieldnames = [
            "invoice_id",
            "vendor_id",
            "due_date",
            "payment_date",
            "payment_amount",
            "payment_status"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(payment_records)

    print("PAYMENT REGISTER GENERATION")
    print("---------------------------")
    print("Total invoices loaded:", len(invoices))
    print("Total payment records:", len(payment_records))
    print("Payment register generated successfully!")
    

if __name__ == "__main__":
    main()
