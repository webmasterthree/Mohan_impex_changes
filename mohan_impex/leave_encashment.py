import frappe
from frappe.utils.safe_exec import safe_eval

@frappe.whitelist()
def get_formula(emp):
    data = frappe.db.sql("""
        SELECT ss.custom_formula
        FROM `tabSalary Structure Assignment` ssa
        LEFT JOIN `tabSalary Structure` ss
            ON ss.name = ssa.salary_structure AND ss.custom_leave_encashment = "Formula Base"
        WHERE ssa.employee = %s
    """, (emp,), as_dict=True)

    return data



def validate(self, event):
    set_encashment_amount(self)


def set_encashment_amount(self):

    if not hasattr(self, "_salary_structure"):
        self.set_salary_structure()

    # 👉 Salary Structure se setting lao
    leave_mode, formula = frappe.db.get_value(
        "Salary Structure",
        self._salary_structure,
        ["custom_leave_encashment", "custom_formula"]
    )

    # -----------------------------------
    # 👉 Case 1 : Formula Base
    # -----------------------------------
    if leave_mode == "Formula Base" and formula:

        # Base fetch karo
        base = frappe.get_value(
            "Salary Structure Assignment",
            filters={
                "employee": self.employee,
                "salary_structure": self._salary_structure,
                "docstatus": 1,
                "from_date": ["<=", self.encashment_date],
            },
            fieldname="base",
            order_by="from_date desc",
        ) or 0

        context = {
            "base": base,
            "encashment_days": self.encashment_days,
            "days": self.encashment_days,
            "doc": self,
        }

        self.encashment_amount = safe_eval(formula, context)
        return

    # -----------------------------------
    # 👉 Case 2 : Fix Amount (Existing)
    # -----------------------------------
    per_day_encashment = frappe.get_value(
        "Salary Structure Assignment",
        filters={
            "employee": self.employee,
            "salary_structure": self._salary_structure,
            "docstatus": 1,
            "from_date": ["<=", self.encashment_date],
        },
        fieldname="leave_encashment_amount_per_day",
        order_by="from_date desc",
    )

    if not per_day_encashment:
        per_day_encashment = frappe.db.get_value(
            "Salary Structure",
            self._salary_structure,
            "leave_encashment_amount_per_day",
        )

    per_day_encashment = per_day_encashment or 0

    self.encashment_amount = (
        self.encashment_days * per_day_encashment
        if per_day_encashment > 0 else 0
    )
