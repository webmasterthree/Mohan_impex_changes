import frappe
from frappe.utils import getdate
from datetime import timedelta
from mohan_impex.mohan_impex.report.daily_attendance_whatsapp_report import get_approved_leave_applications

def execute(filters=None):
    """
    Generates a structured leave and work-from-home report with the following sections:
    1. "LEAVE TODAY"
    2. "WFH TODAY"
    3. "UPCOMING LEAVE"
    4. "UPCOMING WFH"

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
        {"fieldname": "to_date", "label": "TO", "fieldtype": "Data", "width": 180},
    ]

    # Extract data
    leave_applications = leave_data.get("leave_applications", [])
    work_from_home_applications = leave_data.get("work_from_home_applications", [])

    # Categorized lists
    leave_today, upcoming_leave, wfh_today, upcoming_wfh = [], [], [], []

    # Function to clean department names
    def clean_department(department):
        if department and department.endswith(" - MISL"):
            return department.replace(" - MISL", "")
        return department

    # Function to format date as dd-mm-yyyy
    def format_date(date_str):
        if date_str:
            return getdate(date_str).strftime("%d-%m-%Y")
        return ""

    # --------------------------
    # Process leave applications
    # --------------------------
    for entry in leave_applications:
        if not all(k in entry for k in ["from_date", "to_date", "employee_name", "total_leave_days"]):
            continue  # Skip malformed data

        from_date, to_date = getdate(entry["from_date"]), getdate(entry["to_date"])

        # store raw date for sorting later
        entry["raw_from_date"] = from_date

        # Duration (string)
        entry["formatted_duration"] = f"{float(entry['total_leave_days'])}"

        # Clean department name
        entry["department"] = clean_department(entry.get("department", ""))

        # Format dates for display
        entry["from_date"] = format_date(entry["from_date"])
        entry["to_date"] = format_date(entry["to_date"])

        # Categorize
        if from_date <= today <= to_date:
            leave_today.append(entry)
        elif from_date > today:
            upcoming_leave.append(entry)

    # ------------------------------------
    # Process work-from-home applications
    # ------------------------------------
    for entry in work_from_home_applications:
        if not all(k in entry for k in ["from_date", "to_date", "employee_name"]):
            continue  # Skip malformed data

        from_date, to_date = getdate(entry["from_date"]), getdate(entry["to_date"])

        # store raw date for sorting later
        entry["raw_from_date"] = from_date

        total_days = abs((to_date - from_date).days) + 1
        entry["formatted_duration"] = f"{float(total_days)}"

        # Clean department name
        entry["department"] = clean_department(entry.get("department", ""))

        # Format dates for display
        entry["from_date"] = format_date(entry["from_date"])
        entry["to_date"] = format_date(entry["to_date"])

        # Categorize
        if from_date <= today <= to_date:
            wfh_today.append(entry)
        elif from_date > today:
            upcoming_wfh.append(entry)

    # ------------------------------
    # Sorting each category properly
    # ------------------------------
    # Use raw_from_date (real date object) for ascending sort,
    # then employee_name as tiebreaker.
    for category in [leave_today, upcoming_leave, wfh_today, upcoming_wfh]:
        category.sort(key=lambda x: (x["raw_from_date"], x["employee_name"]))

    # Section Headers (In Required Order) – no color/indicator
    section_headers = [
        {"category": "leave_today", "label": "LEAVE TODAY", "data": leave_today},
        {"category": "wfh_today", "label": "WFH TODAY", "data": wfh_today},
        {"category": "upcoming_leave", "label": "UPCOMING LEAVE", "data": upcoming_leave},
        {"category": "upcoming_wfh", "label": "UPCOMING WFH", "data": upcoming_wfh},
    ]

    # Construct Final Data in Required Order
    final_data = []
    for section in section_headers:
        if section["data"]:
            # Section row (no indicator field now)
            final_data.append({
                "employee_name": section["label"],
                "is_section": 1,
            })
            # Data rows (already sorted)
            final_data.extend(section["data"])

    return columns, final_data
