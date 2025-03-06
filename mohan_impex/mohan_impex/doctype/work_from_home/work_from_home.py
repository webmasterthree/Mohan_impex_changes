# Copyright (c) 2025, Edubild and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class WorkFromHome(Document):
# 	pass


import frappe
from frappe.model.document import Document
from frappe import _

class WorkFromHome(Document):
    def on_submit(self):
        # Ensure the status is either 'Approved' or 'Rejected' before submission
        if self.status not in ["Approved", "Rejected"]:
            frappe.throw(_("Only Work From Home Requests with status 'Approved' or 'Rejected' can be submitted."))

        # if self.status == "Approved":
        #     # Create a new Shift Assignment document
        #     assignment_doc = frappe.new_doc("Shift Assignment")
        #     assignment_doc.shift_type = "Work From Home"
        #     assignment_doc.employee = self.employee
        #     assignment_doc.start_date = self.from_date

        #     # Set end date if it exists
        #     if self.to_date:
        #         assignment_doc.end_date = self.to_date

        #     # Link the shift request to the Work From Home request
        #     # assignment_doc.shift_request = self.name

        #     # Ignore permissions for this operation
        #     assignment_doc.flags.ignore_permissions = 1
        #     assignment_doc.insert()
        #     assignment_doc.submit()

        #     # Display a success message
        #     frappe.msgprint(
        #         _("Shift Assignment: {0} created for Employee: {1}").format(
        #             frappe.bold(assignment_doc.name), frappe.bold(self.employee)
        #         )
        #     )
