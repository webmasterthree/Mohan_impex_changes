from erpnext.stock.doctype.quality_inspection.quality_inspection import QualityInspection as ParentQualityInspection
import frappe

class QualityInspection(ParentQualityInspection):
	def update_qc_reference(self):
		quality_inspection = self.name if self.docstatus == 1 else ""

		if self.reference_type == "Job Card":
			if self.reference_name:
				frappe.db.sql(
					f"""
					UPDATE `tab{self.reference_type}`
					SET quality_inspection = %s, modified = %s
					WHERE name = %s and production_item = %s
				""",
					(quality_inspection, self.modified, self.reference_name, self.item_code),
				)

		else:
			args = [quality_inspection, self.modified, self.reference_name, self.item_code]
			doctype = self.reference_type + " Item"

			if self.reference_type == "Stock Entry":
				doctype = "Stock Entry Detail"

			if self.reference_type and self.reference_name:
				conditions = ""
				if self.inspection_scope == "Product":
					updatefield = "t1.product_inspection"
				elif self.inspection_scope == "Application":
					updatefield = "t1.application_inspection"
				else:
					updatefield = "t1.quality_inspection"
				if self.batch_no and self.docstatus == 1:
					conditions += " and t1.batch_no = %s"
					args.append(self.batch_no)

				if self.docstatus == 2:  # if cancel, then remove qi link wherever same name
					conditions += f" and {updatefield} = %s"
					args.append(self.name)

				frappe.db.sql(
					f"""
					UPDATE
						`tab{doctype}` t1, `tab{self.reference_type}` t2
					SET
						{updatefield} = %s, t2.modified = %s
					WHERE
						t1.parent = %s
						and t1.item_code = %s
						and t1.parent = t2.name
						{conditions}
				""",
					args,
				)
		
