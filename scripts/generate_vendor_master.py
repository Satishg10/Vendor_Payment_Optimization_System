import csv # Create and write CSV files
import random # Generate varied vendor information
from datetime import date , timedelta # Work with dates, Calculate date differences
from pathlib import Path # Locate project folders and files

# random will help us select different cities, vendor categories and payment terms.


# Project configuration

TOTAL_VENDORS = 150 # Defines how many vendor records.

RANDOM_SEED = 42 # Ensures reproducibility.
# If you execute the script multiple times without changing the seed, 
# the random selections will remain consistent.


random.seed(RANDOM_SEED) 
# Initializes Python's random number generator using our fixed seed.



# Vendor categories

# Why? Every vendor will belong to one of these eight categories.

VENDOR_CATEGORIES = [
    "IT Services",
    "Office Supplies",
    "Logistics",
    "Facility Management",
    "Raw Materials",
    "Marketing",
    "Consulting",
    "Equipment"
]


# Indian cities and their respective states.

# Why use a dictionary?
# Because each city is associated with a particular state.

CITY_STATE_MAPPING = {
    "Bengaluru": "Karnataka",
    "Mysuru": "Karnataka",
    "Mumbai": "Maharashtra",
    "Pune": "Maharashtra",
    "Hyderabad": "Telangana",
    "Chennai": "Tamil Nadu",
    "Delhi": "Delhi",
    "Kochi": "Kerala",
    "Ahmedabad": "Gujarat",
    "Jaipur": "Rajasthan"
}


# Define Vendor payment terms
# These represent the contractual number of days within which 
# vendors should receive payment.
PAYMENT_TERMS = [
    "Net 15",
    "Net 30",
    "Net 45",
    "Net 60"
]


# Vendor registration status
# These statuses will help us analyse active and inactive vendors later
VENDOR_STATUSES = [
    "Active",
    "Inactive",
    "Under Review"
]



# Vendor name components

VENDOR_PREFIXES = [
    "Apex",
    "Global",
    "Prime",
    "Reliable",
    "United",
    "Dynamic",
    "Smart",
    "Elite",
    "Supreme",
    "NextGen",
    "Vertex",
    "Innovative"
]

VENDOR_SUFFIXES = [
    "Solutions",
    "Enterprises",
    "Industries",
    "Services",
    "Technologies",
    "Associates",
    "Corporation",
    "Systems",
    "Traders",
    "Consultants"
]


# Simulated vendor email domains

EMAIL_DOMAINS = [
    "example.com",
    "example.org",
    "example.net"
]

# Function to generate unique vendor names

def generate_vendor_name(vendor_number):

    prefix = random.choice(VENDOR_PREFIXES)
    suffix = random.choice(VENDOR_SUFFIXES)

    vendor_name = f"{prefix} {suffix} {vendor_number:03d}"

    return vendor_name


# Function to generate vendor email addresses

def generate_vendor_email(vendor_name):

    email_name = vendor_name.lower().replace(" ", ".")

    email_domain = random.choice(EMAIL_DOMAINS)

    vendor_email = f"{email_name}@{email_domain}"

    return vendor_email



# Function to generate unique vendor IDs

def generate_vendor_id(vendor_number):

    return f"VND-{vendor_number:04d}"

# Function to generate simulated tax reference IDs

def generate_tax_reference_id(vendor_number):

    return f"SIM-GST-{vendor_number:04d}"


# Function to generate vendor location

def generate_vendor_location():

    city = random.choice(list(CITY_STATE_MAPPING.keys()))

    state = CITY_STATE_MAPPING[city]

    return city, state


# Function to generate vendor registration dates

def generate_registration_date():

    random_days = random.randint(0, 1825)

    registration_date = date.today() - timedelta(days=random_days)

    return registration_date.isoformat()



# Function to generate a complete vendor record

def generate_vendor_record(vendor_number):
    vendor_id = generate_vendor_id(vendor_number)
    vendor_name = generate_vendor_name(vendor_number)
    vendor_category = random.choice(VENDOR_CATEGORIES)
    gstin = generate_tax_reference_id(vendor_number)
    contact_email = generate_vendor_email(vendor_name)
    city, state = generate_vendor_location()
    payment_terms = random.choice(PAYMENT_TERMS)
    vendor_status = random.choice(VENDOR_STATUSES)
    registration_date = generate_registration_date()

    vendor_record = {
        "vendor_id": vendor_id,
        "vendor_name": vendor_name,
        "vendor_category": vendor_category,
        "gstin": gstin,
        "contact_email": contact_email,
        "city": city,
        "state": state,
        "payment_terms": payment_terms,
        "vendor_status": vendor_status,
        "registration_date": registration_date
    }

    return vendor_record

def main():

    # Create an empty list to store vendor records
    vendor_records = []

    # Generate 150 vendor records
    for vendor_number in range(1, TOTAL_VENDORS + 1):
        vendor = generate_vendor_record(vendor_number)
        vendor_records.append(vendor)

    # Define output file path
    output_file = ( 
        Path(__file__).resolve().parents[1]
        # Path(__file__) identifies your current Python script.
        # .resolve() gets its absolute path.
        # .parents[1] moves up to your project root directory.
        / "data" # #/ "data" / "raw" navigates into the raw data folder
        / "raw"
        / "vendor_master.csv" # # / "vendor_master.csv" specifies the output filename.
    )

    # Open CSV file for writing
    with open(output_file, "w", newline="", encoding="utf-8") as file:
# output_file: Where the file will be saved
# "w":	Write mode (creates or overwrites the file)
# newline="":	Prevents unwanted blank rows
# encoding="utf-8":	Supports standard Unicode text
# as file:	Gives us a variable to work with the opened file
        writer = csv.DictWriter(
            file,
            fieldnames=vendor_records[0].keys()
        )
# csv.DictWriter() creates a CSV writer that accepts dictionaries.
# file tells it which file to write into.
# vendor_records[0].keys() retrieves the column names from the first vendor dictionary

        writer.writeheader() # writes the column names.
        writer.writerows(vendor_records) # writes all 150 vendor records.
        print(f"Successfully generated {len(vendor_records)} vendor records.")
        # len(vendor_records) counts the number of vendor records.
        # The f string allows us to insert that count into the message.
        # It confirms that the CSV generation process has completed.


if __name__ == "__main__": # checks whether this Python file is being executed directly.
    main() # starts the main function.











