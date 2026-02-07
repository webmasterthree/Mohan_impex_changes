import frappe
from frappe import _
import json

@frappe.whitelist()
def assign_employees(job_cards, employees):
    job_cards = json.loads(job_cards) if isinstance(job_cards, str) else job_cards
    employees = json.loads(employees)

    for job in job_cards:
        doc = frappe.get_doc("Job Card", job)

        existing = {row.employee for row in doc.employee if row.employee}

        for e in employees:
            if e["employee"] not in existing:
                doc.append("employee", {
                    "employee": e["employee"]
                })

        doc.save(ignore_permissions=True)

    frappe.db.commit()
