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





@frappe.whitelist()
def deduction():
	parent_names = frappe.get_all("Full and Final Statement", pluck="name")

	out = []
	for parent in parent_names:
		doc = frappe.get_doc("Full and Final Statement", parent)

		for d in (doc.payables or []):
			# ✅ Apply filter
			if d.reference_document_type == "Salary Slip":
				out.append({
					"reference_document_type": d.reference_document_type,
					"reference_document": d.reference_document,
					"amount": d.amount
				})

	return out
