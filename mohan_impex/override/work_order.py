import frappe
from frappe.utils import flt
from erpnext.manufacturing.doctype.work_order.work_order import WorkOrder


class CustomWorkOrder(WorkOrder):

    def calculate_operating_cost(self):
        
        super().calculate_operating_cost()

        
        item = frappe.get_cached_doc("Item", self.production_item)

        fixed_total = 0
        if item.custom_total_operation_cost:
            fixed_total = flt(item.custom_total_operation_cost) * flt(self.qty)

        
        self.custom_fixed_operating_cost = fixed_total

        
        self.total_operating_cost = (
            flt(self.additional_operating_cost)
            + flt(self.corrective_operation_cost)
            + flt(self.planned_operating_cost if not self.actual_operating_cost else self.actual_operating_cost)
            + flt(self.custom_fixed_operating_cost)
        )