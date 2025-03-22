import frappe
import json
from collections import defaultdict
from frappe import _

@frappe.whitelist()
def get_unpaid_invoices():
    """
    Fetch all unpaid sales invoices and group them by customer.
    """
    try:
        invoices = frappe.get_all(
            "Sales Invoice",
            filters={"status": "Unpaid"},
            fields=["customer", "due_date", "grand_total"]
        )

        # Group invoices by customer
        grouped_invoices = defaultdict(list)
        for inv in invoices:
            grouped_invoices[inv["customer"]].append({
                "due_date": inv["due_date"].strftime("%Y-%m-%d") if inv["due_date"] else None,
                "grand_total": float(inv["grand_total"])  # Ensure grand_total is float
            })

        # Convert dictionary to structured JSON response
        response_data = [
            {"customer": customer, "invoices": details} for customer, details in grouped_invoices.items()
        ]

        return {
            "status": "success",
            "message": f"Found {len(response_data)} customers with unpaid invoices",
            "data": response_data
        }

    except Exception as e:
        frappe.log_error(f"Error fetching unpaid invoices: {str(e)}", "Unpaid Invoices API")
        return {
            "status": "error",
            "message": "An error occurred while fetching invoices",
            "error": str(e)
        }
