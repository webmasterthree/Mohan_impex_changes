import frappe
from frappe.utils import getdate
from datetime import timedelta
from mohan_impex.mohan_impex.report.daily_attendance_whatsapp_report import get_approved_leave_applications

def execute(filters=None):
    """
    Generates a structured leave and work-from-home report with colored section headers:
    1. "LEAVE TODAY" (highlighted in Yellow)
    2. "WFH TODAY" (highlighted in Blue)
    3. "UPCOMING LEAVE" (highlighted in Green)
    4. "UPCOMING WFH" (highlighted in Purple)

    :param filters: Dictionary containing filter options, e.g., {'from_date': 'YYYY-MM-DD', 'to_date': 'YYYY-MM-DD'}
    :return: Tuple (columns, data) formatted for ERPNext report generation.
    """

    # Get today's date
    today = getdate()

    # Fetch leave and work-from-home data
    leave_data = get_approved_leave_applications()

    # Handle errors
    if not leave_data or leave_data.get("status") != "success":
        frappe.throw("Error fetching leave data: " + leave_data.get("message", "Unknown error"))

    # Define report columns
    columns = [
        {"fieldname": "employee_name", "label": "NAME", "fieldtype": "Data", "width": 250},
        {"fieldname": "department", "label": "DEPARTMENT", "fieldtype": "Data", "width": 250},
        {"fieldname": "location", "label": "LOCATION", "fieldtype": "Data", "width": 180},  
        {"fieldname": "formatted_duration", "label": "NO. OF DAYS", "fieldtype": "Data", "width": 180},
        {"fieldname": "from_date", "label": "FROM", "fieldtype": "Data", "width": 180},
        {"fieldname": "to_date", "label": "TO", "fieldtype": "Data", "width": 180}
    ]

    # Extract data
    leave_applications = leave_data.get("leave_applications", [])
    work_from_home_applications = leave_data.get("work_from_home_applications", [])

    # Categorized lists
    leave_today, upcoming_leave, wfh_today, upcoming_wfh = [], [], [], []

    # Function to clean department names
    def clean_department(department):
        if department and department.endswith(" - MIFOOD"):
            return department.replace(" - MIFOOD", "")
        return department

    # Function to format date as dd-mm-yy
    def format_date(date_str):
        if date_str:
            return getdate(date_str).strftime("%d-%m-%y")
        return ""

    # Process leave applications
    for entry in leave_applications:
        if not all(k in entry for k in ["from_date", "to_date", "employee_name", "total_leave_days"]):
            continue  # Skip malformed data

        from_date, to_date = getdate(entry["from_date"]), getdate(entry["to_date"])
        entry["formatted_duration"] = f"{float(entry['total_leave_days'])}"  # Remove .0

        # Clean department name
        entry["department"] = clean_department(entry.get("department", ""))

        # Format dates
        entry["from_date"] = format_date(entry["from_date"])
        entry["to_date"] = format_date(entry["to_date"])

        if from_date <= today <= to_date:
            leave_today.append(entry)
        elif from_date > today:
            upcoming_leave.append(entry)

    # Process work-from-home applications
    for entry in work_from_home_applications:
        if not all(k in entry for k in ["from_date", "to_date", "employee_name"]):
            continue  # Skip malformed data

        from_date, to_date = getdate(entry["from_date"]), getdate(entry["to_date"])
        total_days = abs((to_date - from_date).days) + 1
        entry["formatted_duration"] = f"{float(total_days)}"  # Remove .0

        # Clean department name
        entry["department"] = clean_department(entry.get("department", ""))

        # Format dates
        entry["from_date"] = format_date(entry["from_date"])
        entry["to_date"] = format_date(entry["to_date"])

        if from_date <= today <= to_date:
            wfh_today.append(entry)
        elif from_date > today:
            upcoming_wfh.append(entry)

    # Sorting each category
    for category in [leave_today, upcoming_leave, wfh_today, upcoming_wfh]:
        category.sort(key=lambda x: (x["from_date"], x["employee_name"]))

    # Section Headers (In Required Order)
    section_headers = [
        {"category": "leave_today", "label": "LEAVE TODAY", "indicator": "yellow", "data": leave_today},
        {"category": "wfh_today", "label": "WFH TODAY", "indicator": "blue", "data": wfh_today},
        {"category": "upcoming_leave", "label": "UPCOMING LEAVE", "indicator": "green", "data": upcoming_leave},
        {"category": "upcoming_wfh", "label": "UPCOMING WFH", "indicator": "purple", "data": upcoming_wfh},
    ]

    # Construct Final Data in Required Order
    final_data = []
    for section in section_headers:
        if section["data"]:
            final_data.append({
                "employee_name": section["label"],
                "is_section": 1,
                "indicator": section["indicator"]
            })
            final_data.extend(section["data"])

    return columns, final_data
