import frappe
from frappe.utils import time_diff_in_hours, get_datetime

def calculate_working_hours(doc, method):
    if doc.status == "Present" and doc.shift:
        shift = frappe.get_doc("Shift Type", doc.shift)
        expected_hours = shift.duration

        if doc.check_in and doc.check_out:
            check_in_time = get_datetime(doc.check_in)
            check_out_time = get_datetime(doc.check_out)
            actual_hours = time_diff_in_hours(check_out_time, check_in_time)

            # Calculate Overtime
            doc.overtime_hours = max(0, actual_hours - expected_hours)

            # Calculate Shortfall
            doc.shortfall_hours = max(0, expected_hours - actual_hours)

            # Save changes
            doc.save()

            # Log calculations for debugging
            frappe.logger().info(f"Attendance {doc.name}: Actual Hours = {actual_hours}, Overtime = {doc.overtime_hours}, Shortfall = {doc.shortfall_hours}")
