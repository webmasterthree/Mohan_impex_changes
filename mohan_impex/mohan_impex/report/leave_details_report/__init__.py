import frappe
from frappe.utils import getdate
from collections import defaultdict

@frappe.whitelist()
def get_employee_leave_report(start_date=None, end_date=None):
    """
    Fetches detailed leave report for employees within a payroll period.
    
    - Includes leave carry forward (b/f)
    - Tracks leave allotment, leaves availed, and LOP (Loss of Pay)
    - Computes closing balances for all leave types
    """

    try:
        # Validate input dates
        if not start_date or not end_date:
            return {"status": "error", "message": "Please provide both start_date and end_date."}

        start_date = getdate(start_date)
        end_date = getdate(end_date)

        if start_date > end_date:
            return {"status": "error", "message": "Start date cannot be greater than end date."}

        # Fetch Employee Data
        employees = frappe.db.get_all(
            "Employee",
            fields=["name", "employee_name", "department", "branch as location", "date_of_joining", "employment_type"]
        )

        # Fetch Leave Allocations
        leave_allocations = frappe.db.get_all(
            'Leave Allocation',
            filters={"from_date": ["<=", end_date], "to_date": [">=", start_date]},
            fields=[
                'employee',
                'leave_type',
                'carry_forwarded_leaves_count',
                'new_leaves_allocated'
            ]
        )

        # Fetch Leave Applications (Availed Leaves)
        leaves_availed = frappe.db.get_all(
            "Leave Application",
            filters={"status": "Approved", "from_date": ["<=", end_date], "to_date": [">=", start_date]},
            fields=["employee", "leave_type", "total_leave_days"]
        )

        # Fetch Loss of Pay (LOP)
        lop_records = frappe.db.get_all(
            "Leave Application",
            filters={"status": "Approved", "leave_type": "Loss of Pay", "from_date": ["<=", end_date], "to_date": [">=", start_date]},
            fields=["employee", "total_leave_days"]
        )

        # Fetch Compensatory Off Availed
        comp_offs_availed = frappe.db.get_all(
            "Leave Application",
            filters={"status": "Approved", "leave_type": "Compensatory Off", "from_date": ["<=", end_date], "to_date": [">=", start_date]},
            fields=["employee", "total_leave_days"]
        )

        # Structure Data
        leave_report = {}

        for emp in employees:
            emp_id = emp["name"]
            leave_report[emp_id] = {
                "Employee Code": emp_id,
                "Employee Name": emp["employee_name"],
                "Department": emp["department"],
                "Location": emp["location"],
                "Date of Joining": emp["date_of_joining"],
                "Employment Type": emp["employment_type"],

                # Carry Forwarded Leaves (b/f)
                "CL b/f": 0, "SL b/f": 0, "EL b/f": 0, "CW b/f": 0,

                # New Leave Allotments
                "CL alloted": 0, "SL alloted": 0, "EL alloted": 0, "CW added": 0,

                # Availed Leaves
                "CL Avail": 0, "SL Avail": 0, "EL Avail": 0, "Comp Offs availed": 0,

                # Loss of Pay (LOP)
                "LOP - current (27-26th)": 0,
                "LOP - c/f to adjust": 0,

                # Total leaves availed
                "Total leaves availed": 0,

                # Closing Balance Calculation
                "CL CLOSING BALANCE": 0, "SL C/f": 0, "EL C/f": 0
            }

        # Process Leave Allocations (b/f and allotted)
        for record in leave_allocations:
            emp_id = record["employee"]
            leave_type = record["leave_type"]

            if emp_id in leave_report:
                if leave_type == "Casual Leave":
                    leave_report[emp_id]["CL b/f"] = record["carry_forwarded_leaves_count"]
                    leave_report[emp_id]["CL alloted"] = record["new_leaves_allocated"]
                elif leave_type == "Sick Leave":
                    leave_report[emp_id]["SL b/f"] = record["carry_forwarded_leaves_count"]
                    leave_report[emp_id]["SL alloted"] = record["new_leaves_allocated"]
                elif leave_type == "Earned Leave":
                    leave_report[emp_id]["EL b/f"] = record["carry_forwarded_leaves_count"]
                    leave_report[emp_id]["EL alloted"] = record["new_leaves_allocated"]
                elif leave_type == "Compensatory Off":
                    leave_report[emp_id]["CW b/f"] = record["carry_forwarded_leaves_count"]
                    leave_report[emp_id]["CW added"] = record["new_leaves_allocated"]

        # Process Leaves Availed
        for record in leaves_availed:
            emp_id = record["employee"]
            leave_type = record["leave_type"]
            if emp_id in leave_report:
                if leave_type == "Casual Leave":
                    leave_report[emp_id]["CL Avail"] += record["total_leave_days"]
                elif leave_type == "Sick Leave":
                    leave_report[emp_id]["SL Avail"] += record["total_leave_days"]
                elif leave_type == "Earned Leave":
                    leave_report[emp_id]["EL Avail"] += record["total_leave_days"]

        # Process Comp Off Availed
        for record in comp_offs_availed:
            emp_id = record["employee"]
            if emp_id in leave_report:
                leave_report[emp_id]["Comp Offs availed"] += record["total_leave_days"]

        # Process Loss of Pay (LOP)
        for record in lop_records:
            emp_id = record["employee"]
            if emp_id in leave_report:
                leave_report[emp_id]["LOP - current (27-26th)"] += record["total_leave_days"]

        # Calculate Closing Balance
        for emp_id, data in leave_report.items():
            data["Total leaves availed"] = (
                data["CL Avail"] + data["SL Avail"] + data["EL Avail"] + data["Comp Offs availed"]
            )

            data["CL CLOSING BALANCE"] = max(0, data["CL b/f"] + data["CL alloted"] - data["CL Avail"])
            data["SL C/f"] = max(0, data["SL b/f"] + data["SL alloted"] - data["SL Avail"])
            data["EL C/f"] = max(0, data["EL b/f"] + data["EL alloted"] - data["EL Avail"])

        return {"status": "success", "data": list(leave_report.values())}

    except Exception as e:
        frappe.log_error(f"Error in get_employee_leave_report: {str(e)}", "Employee Leave Report API")
        return {"status": "error", "message": str(e)}
