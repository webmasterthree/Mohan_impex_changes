import frappe
from frappe.utils import getdate

@frappe.whitelist()
def get_approved_leave_applications(from_date=None, to_date=None):
    """
    Fetches all approved leave applications and work-from-home applications within a specified date range,
    including department and location.

    :param from_date: (Optional) Start date for filtering applications.
    :param to_date: (Optional) End date for filtering applications.
    :return: JSON response containing approved leave and work-from-home applications.
    """
    try:
        leave_filters = {"status": "Approved"}
        wfh_filters = {"status": "Approved"}

        # Apply date filters if provided
        if from_date:
            leave_filters["from_date"] = [">=", from_date]
            wfh_filters["from_date"] = [">=", from_date]
        if to_date:
            leave_filters["to_date"] = ["<=", to_date]
            wfh_filters["to_date"] = ["<=", to_date]

        # Fetch approved leave applications with department and location (branch)
        leave_applications = frappe.db.sql("""
            SELECT 
                la.employee_name,
                la.department,   
                emp.branch AS location,  -- Get branch as location from Employee
                la.from_date,
                la.to_date,
                la.total_leave_days
            FROM `tabLeave Application` la
            LEFT JOIN `tabEmployee` emp ON la.employee = emp.name
            WHERE la.status = 'Approved'
            AND la.docstatus = 1
            {from_date_filter}
            {to_date_filter}
            ORDER BY la.from_date ASC
        """.format(
            from_date_filter=f"AND la.from_date >= '{from_date}'" if from_date else "",
            to_date_filter=f"AND la.to_date <= '{to_date}'" if to_date else ""
        ), as_dict=True)

        # Fetch approved work-from-home applications with department and branch
        wfh_applications = frappe.db.sql("""
            SELECT 
                wfh.employee_name,
                emp.department, 
                emp.branch AS location, 
                wfh.from_date, 
                wfh.to_date
            FROM `tabWork From Home` wfh
            LEFT JOIN `tabEmployee` emp ON wfh.employee = emp.name
            WHERE wfh.status = 'Approved'
            AND wfh.docstatus = 1
            {from_date_filter}
            {to_date_filter}
            ORDER BY wfh.from_date ASC
        """.format(
            from_date_filter=f"AND wfh.from_date >= '{from_date}'" if from_date else "",
            to_date_filter=f"AND wfh.to_date <= '{to_date}'" if to_date else ""
        ), as_dict=True)

        return {
            "status": "success",
            "leave_applications": leave_applications,
            "work_from_home_applications": wfh_applications
        }

    except Exception as e:
        frappe.log_error(f"Error in get_approved_leave_applications: {str(e)}", "Leave API Error")
        return {"status": "error", "message": str(e)}
