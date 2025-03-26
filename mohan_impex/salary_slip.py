import frappe

def handle_pf_on_submit(doc, method):
    import math

    # Components to exclude from total_deduction
    exclude_components = [
        "Provident Fund",
        "Employees State Insurance Corporation"
    ]

    # Total of the excluded deduction components
    excluded_amount = sum(
        d.amount for d in doc.deductions if d.salary_component in exclude_components
    )

    if excluded_amount:
        updated_total_deduction = doc.total_deduction - excluded_amount
        updated_net_pay = doc.gross_pay - updated_total_deduction
        rounded_total = round(updated_net_pay)  # Rounding to nearest rupee

        # Update fields directly in the DB
        doc.db_set("total_deduction", updated_total_deduction)
        doc.db_set("net_pay", updated_net_pay)
        doc.db_set("rounded_total", rounded_total)

        frappe.msgprint(
            f"net_pay: ₹{updated_net_pay}"
        )

# import frappe

# def handle_pf_on_submit(doc, method):
#     # Components to exclude from total_deduction
#     exclude_components = [
#         "Provident Fund",
#         "Employees State Insurance Corporation"
#     ]

#     # Total of the excluded deduction components
#     excluded_amount = sum(
#         d.amount for d in doc.deductions if d.salary_component in exclude_components
#     )

#     if excluded_amount:
#         updated_total_deduction = doc.total_deduction - excluded_amount
#         updated_net_pay = doc.gross_pay - updated_total_deduction

#         # Update fields directly in the DB
#         doc.db_set("total_deduction", updated_total_deduction)
#         doc.db_set("net_pay", updated_net_pay)

#         frappe.msgprint(
#             f"Excluded {', '.join(exclude_components)} (₹{excluded_amount}) from total_deduction.\n"
#             f"Updated total_deduction: ₹{updated_total_deduction}, net_pay: ₹{updated_net_pay}"
#         )
