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
            doctype = self.reference_type + " Item"

            if self.reference_type == "Stock Entry":
                doctype = "Stock Entry Detail"

            if doctype and self.reference_name:
                child_doc = frappe.qb.DocType(doctype)
                if self.inspection_scope == "Product":
                    updatefield = child_doc.product_inspection
                elif self.inspection_scope == "Application":
                    updatefield = child_doc.application_inspection
                else:
                    updatefield = child_doc.quality_inspection
                query = (
                    frappe.qb.update(child_doc)
                    .set(updatefield, quality_inspection)
                    .where(
                        (child_doc.parent == self.reference_name) & (child_doc.item_code == self.item_code)
                    )
                )

                if self.batch_no and self.docstatus == 1:
                    query = query.where(child_doc.batch_no == self.batch_no)

                if self.docstatus == 2:  # if cancel, then remove qi link wherever same name
                    query = query.where(child_doc.quality_inspection == self.name)

                if self.child_row_reference:
                    query = query.where(child_doc.name == self.child_row_reference)

                query.run()

                frappe.db.set_value(
                    self.reference_type,
                    self.reference_name,
                    "modified",
                    self.modified,
                )
