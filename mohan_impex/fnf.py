import frappe
from frappe.utils import date_diff

@frappe.whitelist()
def settlement_period():
    names = frappe.get_all("Full and Final Statement", pluck="name")

    out = []
    for name in names:
        doc = frappe.get_doc("Full and Final Statement", name)

        payables = []
        for d in (doc.payables or []):
            ref_dt = d.reference_document_type
            ref_dn = d.reference_document

            settlement_days = None

            if ref_dt and ref_dn and frappe.db.exists(ref_dt, ref_dn):
                meta = frappe.get_meta(ref_dt)

                # 1️⃣ start_date & end_date
                if meta.has_field("start_date") and meta.has_field("end_date"):
                    vals = frappe.db.get_value(
                        ref_dt, ref_dn, ["start_date", "end_date"], as_dict=True
                    ) or {}

                    start_date = vals.get("start_date")
                    end_date = vals.get("end_date")

                    if start_date and end_date:
                        settlement_days = date_diff(end_date, start_date)

                # 2️⃣ encashment_days
                elif meta.has_field("encashment_days"):
                    settlement_days = frappe.db.get_value(
                        ref_dt, ref_dn, "encashment_days"
                    )

                # 3️⃣ current_work_experience
                elif meta.has_field("current_work_experience"):
                    settlement_days = frappe.db.get_value(
                        ref_dt, ref_dn, "current_work_experience"
                    )

            payables.append({
                "reference_document_type": ref_dt,
                "reference_document": ref_dn,
                "settlement_period_days": settlement_days or 0,  # 👈 converts None to 0
            })

        out.append({
            "name": doc.name,
            "payables": payables
        })

    return out





import frappe
from frappe.utils import flt

@frappe.whitelist()
def deduction(name):
    if not name:
        return []

    fnf = frappe.get_doc("Full and Final Statement", name)

    out = []
    for p in (fnf.payables or []):
        if p.reference_document_type != "Salary Slip" or not p.reference_document:
            continue

        slip_name = p.reference_document

        # 🔹 Fetch Salary Slip (better than db.get_value if you extend later)
        slip_doc = frappe.get_doc("Salary Slip", slip_name)

        payment_days = flt(slip_doc.payment_days)

        deduction_rows = frappe.db.get_all(
            "Salary Detail",
            filters={
                "parent": slip_name,
                "parenttype": "Salary Slip",
                "parentfield": "deductions",
            },
            fields=["salary_component", "amount"],
            order_by="idx asc",
        )

        deductions = []
        for d in deduction_rows:
            amount = flt(d.get("amount"))

            # Optional: skip zero rows
            if amount == 0:
                continue

            deductions.append({
                "salary_component": d.get("salary_component"),
                "amount": amount,
                "days": payment_days,
                "rate": round((amount / payment_days), 2) if payment_days else 0
            })

        # 🔹 Total Deduction
        total_deduction = sum(d["amount"] for d in deductions)

        out.append({
            "fnf": name,
            "salary_slip": slip_name,
            "payment_days": payment_days,
            "fnf_payable_amount": flt(p.amount),
            "total_deduction": total_deduction,
            "net_amount": flt(p.amount) - total_deduction,
            "deductions": deductions
        })

    return out