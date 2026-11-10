# Data Dictionary

## 1. Vendor Master

| Field           | Description                         |
| --------------- | ----------------------------------- |
| vendor_id       | Unique vendor identifier            |
| vendor_name     | Vendor or supplier name             |
| gstin           | Simulated GST identification number |
| vendor_category | Type of supplier                    |
| contact_email   | Vendor contact email                |
| payment_terms   | Contractual payment terms in days   |
| vendor_status   | Active or inactive                  |

## 2. Purchase Order Register

| Field     | Description                      |
| --------- | -------------------------------- |
| po_id     | Unique purchase order identifier |
| vendor_id | Reference to vendor master       |
| po_date   | Purchase order creation date     |
| po_amount | Approved purchase order amount   |
| po_status | Open, closed or cancelled        |

## 3. Invoice Register

| Field                 | Description                                    |
| --------------------- | ---------------------------------------------- |
| invoice_id            | Unique internal invoice identifier             |
| vendor_id             | Reference to vendor master                     |
| po_id                 | Reference to purchase order                    |
| vendor_invoice_number | Invoice number provided by vendor              |
| invoice_date          | Date printed on invoice                        |
| received_date         | Date invoice was first received                |
| complete_invoice_date | Date all required documents were received      |
| invoice_amount        | Invoice amount                                 |
| verification_status   | Pending, verified or rejected                  |
| exception_reason      | Reason for an invoice exception                |
| payment_ready_date    | Date invoice became approved and payment-ready |

## 4. Approval Log

| Field                    | Description                       |
| ------------------------ | --------------------------------- |
| approval_id              | Unique approval record identifier |
| invoice_id               | Reference to invoice register     |
| approver_name            | Person responsible for approval   |
| approval_submission_date | Date approval was requested       |
| approval_date            | Date approval was completed       |
| approval_status          | Pending, approved or rejected     |

## 5. Payment Register

| Field                 | Description                     |
| --------------------- | ------------------------------- |
| payment_id            | Unique payment identifier       |
| invoice_id            | Reference to invoice register   |
| due_date              | Contractual payment due date    |
| payment_date          | Actual payment release date     |
| payment_amount        | Amount paid                     |
| payment_status        | Pending, paid or overdue        |
| transaction_reference | Simulated transaction reference |

## 6. Data Integrity Rules

1. Every vendor must have a unique vendor ID.
2. Every invoice must have a unique internal invoice ID.
3. Vendor invoice numbers must be checked for duplicates within each vendor.
4. Every valid PO reference must exist in the purchase order register.
5. Invoice amounts must be positive.
6. Approval records must reference valid invoices.
7. Payment records must reference valid invoices.
8. Payment dates cannot precede payment-ready dates.
9. Incomplete invoices must not enter the approved payment-ready stage.

## 7. KPI Definitions

### Average Processing Time

Average calendar days between complete_invoice_date and payment_ready_date for completed invoices.

### On-Time Payment Rate

Number of invoices paid on or before their contractual due dates divided by the number of paid invoices, multiplied by 100.

### Overdue Invoices

Invoices whose contractual due date has passed and which remain unpaid.

### Duplicate Invoice Count

Number of vendor invoice submissions flagged as potential duplicates.

## 8. Dataset Information

- All records are simulated.
- No real vendor or banking information is used.
- Planned invoice volume: 500 records.
- Planned vendor volume: 150 records.
