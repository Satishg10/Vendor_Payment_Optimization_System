import csv # Reads CSV files
from pathlib import Path # Locates project folders
# datetime - Converts text into dates
# timedelta - Calculates date differences
from datetime import datetime, timedelta 

# Function to load CSV data
def load_csv(file_path):
    with open(file_path, "r", newline="", encoding="utf-8") as file:
      # open() - Opens the CSV file.
      # "r" - Opens it in read mode.
        reader = csv.DictReader(file)
        # csv.DictReader() - Reads each row as a dictionary
        return list(reader) # Converts all rows into a Python list and 
        # Sends the list back to whoever calls the function. 

# Locate project root directory
project_root = Path(__file__).resolve().parents[1]
# parents[1] - Moves from scripts folder to project root

# Define input file paths
vendor_file = (
    project_root
    / "data"
    / "raw"
    / "vendor_master.csv"
)

invoice_file = (
    project_root
    / "data"
    / "processed"
    / "invoice_transactions.csv"
)

# Main function to load and inspect datasets
def main():
    # Load vendor records
    vendors = load_csv(vendor_file)

    # Load invoice records
    invoices = load_csv(invoice_file)
    
    # Display dataset information
    print("DATASET VALIDATION")
    print("-------------------------")
    print("Total vendors:", len(vendors))
    print("Total invoices:", len(invoices))

    # Check for duplicate vendor IDs
    vendor_ids = [row["vendor_id"] for row in vendors]
    unique_vendor_ids = set(vendor_ids)

    # Check for duplicate invoice IDs
    invoice_ids = [row["invoice_id"] for row in invoices]
    unique_invoice_ids = set(invoice_ids)

    # Check whether invoices reference valid vendors
    invoice_vendor_ids = {row["vendor_id"] for row in invoices}
    invalid_vendor_ids = invoice_vendor_ids - unique_vendor_ids

    print("\nDATA QUALITY CHECKS")
    print("-------------------------")
    print("Duplicate vendor IDs:", len(vendor_ids) - len(unique_vendor_ids))
    print("Duplicate invoice IDs:", len(invoice_ids) - len(unique_invoice_ids))
    print("Invalid vendor references:", len(invalid_vendor_ids))


    # Check for missing values in vendor records
    required_vendor_columns = [
        "vendor_id",
        "vendor_name",
        "gstin",
        "contact_email"
    ]

    missing_vendor_values = sum(
        1
        for row in vendors
        for column in required_vendor_columns
        if not row[column].strip()
    )

    # Check for missing values in invoice records
    required_invoice_columns = [
        "invoice_id",
        "vendor_id",
        "invoice_date",
        "due_date",
        "payment_terms",
        "invoice_amount"
    ]

    missing_invoice_values = sum(
        1
        for row in invoices
        for column in required_invoice_columns
        if not row[column].strip()
    )

    print("\nMISSING VALUE CHECKS")
    print("-------------------------")
    print("Missing vendor values:", missing_vendor_values)
    print("Missing invoice values:", missing_invoice_values)

    # Check invoice and due dates
    invalid_dates = 0

    for invoice in invoices:

        try:
            invoice_date = datetime.strptime(
                invoice["invoice_date"], "%Y-%m-%d"
            )

            due_date = datetime.strptime(
                invoice["due_date"], "%Y-%m-%d"
            )

            if due_date < invoice_date:
                invalid_dates += 1

        except ValueError:
            invalid_dates += 1

    print("\nDATE VALIDATION")
    print("--------------------------")
    print("Invalid date records:", invalid_dates)


# Execute main function
if __name__ == "__main__":
    main()