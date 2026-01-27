import frappe

def validate(doc,method):
    slry_holding = slry_holding = frappe.db.sql("""SELECT employee, number_of_withholding_cycles, from_date, to_date FROM `tabSalary Withholding`WHERE employee = %s""", (doc.employee,), as_dict=True)
    ffs_outstanding_statement = frappe.db.sql("""SELECT reference_document FROM `tabFull and Final Outstanding Statement` WHERE parent = %s AND reference_document_type = 'Salary Slip' """, (doc.name,), as_dict=True)
    print("------------------------------------------------",ffs_outstanding_statement)


@frappe.whitelist()
def get_account_and_amount(ref_doctype, ref_document, company):
	if not ref_doctype or not ref_document:
		return None

	if ref_doctype == "Salary Slip":
		salary_details = frappe.db.get_value(
			"Salary Slip", ref_document, ["payroll_entry", "net_pay"], as_dict=1
		)
		amount = salary_details.net_pay
		payable_account = (
			frappe.db.get_value("Payroll Entry", salary_details.payroll_entry, "payroll_payable_account")
			if salary_details.payroll_entry
			else None
		)
		return [payable_account, amount]

	if ref_doctype == "Gratuity":
		payable_account, amount = frappe.db.get_value("Gratuity", ref_document, ["payable_account", "amount"])
		return [payable_account, amount]

	if ref_doctype == "Expense Claim":
		details = frappe.db.get_value(
			"Expense Claim",
			ref_document,
			["payable_account", "grand_total", "total_amount_reimbursed", "total_advance_amount"],
			as_dict=True,
		)
		payable_account = details.payable_account
		amount = details.grand_total - (details.total_amount_reimbursed + details.total_advance_amount)
		return [payable_account, amount]

	if ref_doctype == "Loan":
		details = frappe.db.get_value(
			"Loan", ref_document, ["payment_account", "total_payment", "total_amount_paid"], as_dict=1
		)
		payment_account = details.payment_account
		amount = details.total_payment - details.total_amount_paid
		return [payment_account, amount]

	if ref_doctype == "Employee Advance":
		details = frappe.db.get_value(
			"Employee Advance",
			ref_document,
			["advance_account", "paid_amount", "claimed_amount", "return_amount"],
			as_dict=1,
		)
		payment_account = details.advance_account
		amount = details.paid_amount - (details.claimed_amount + details.return_amount)
		return [payment_account, amount]

	if ref_doctype == "Leave Encashment":
		amount = frappe.db.get_value("Leave Encashment", ref_document, "encashment_amount")
		payable_account = frappe.get_cached_value("Company", company, "default_payroll_payable_account")
		return [payable_account, amount]
	
    
	if ref_doctype == "Notice Period Buyout":
		amount = frappe.db.get_value("Notice Period Buyout", ref_document, "amount")
		payable_account = frappe.get_cached_value("Company", company, "default_payroll_payable_account")
		return [payable_account, amount]




@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_reference_doctypes(doctype, txt, searchfield, start, page_len, filters):
    modules = ["HR", "Payroll", "Loan Management"]
    
    return frappe.db.sql("""
        SELECT name 
        FROM `tabDocType`
        WHERE istable = 0 
        AND issingle = 0
        AND (module IN %(modules)s OR name = 'Notice Period Buyout')
        AND name LIKE %(txt)s
        ORDER BY name
        LIMIT %(page_len)s OFFSET %(start)s
    """, {
        'modules': modules,
        'txt': f'%{txt}%',
        'page_len': page_len,
        'start': start
    })



@frappe.whitelist()
def get_buyout_doc(employee):
    doc = frappe.get_all(
        "Notice Period Buyout",
        filters={"employee": employee},
        fields=["name"],
        limit=1
    )

    if not doc:
        return None

    return frappe.get_doc("Notice Period Buyout", doc[0].name)
