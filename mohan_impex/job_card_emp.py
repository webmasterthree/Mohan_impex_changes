import frappe

@frappe.whitelist()
def assign_employee(name=None):
    # Fetching the Job Card data based on the passed 'name' argument
    filters = {}
    if name:
        filters = {"name": name}
    
    job_cards = frappe.db.get_all(
        "Job Card",
        filters=filters,
        fields=["name"],
    )
    
    # Fetching the employee from the child table based on the Job Cards
    job_card_employees = frappe.db.get_all(
        "Job Card Time Log",  # Assuming the child table is "Job Card Time Log"
        filters={"parent": ["in", [job["name"] for job in job_cards]]},
        fields=["parent", "employee"]
    )

    # Create a dictionary to associate Job Card with Employees
    job_card_employee_map = {}
    for entry in job_card_employees:
        if entry["parent"] not in job_card_employee_map:
            job_card_employee_map[entry["parent"]] = []
        job_card_employee_map[entry["parent"]].append(entry["employee"])
    
    # Fetch the user_id for each employee
    job_card_user_map = {}
    for job_card, employees in job_card_employee_map.items():
        job_card_user_map[job_card] = []
        for employee in employees:
            user_id = frappe.db.get_value('Employee', employee, 'user_id')
            job_card_user_map[job_card].append({
                "employee": employee,
                "user_id": user_id
            })
    
    # Combine the job cards with the associated employees and their user_ids
    result = []
    for job in job_cards:
        result.append({
            "job_card": job["name"],
            "employees": job_card_user_map.get(job["name"], [])
        })
    
    return result









# import frappe
# import time
# from frappe.exceptions import QueryDeadlockError

# @frappe.whitelist()
# def assign_employee(name=None):
#     # Maximum retry attempts in case of deadlock
#     max_retries = 3
#     retries = 0
    
#     while retries < max_retries:
#         try:
#             # Fetching the Job Card data based on the passed 'name' argument
#             filters = {}
#             if name:
#                 filters = {"name": name}
            
#             # Fetch the job card details
#             job_cards = frappe.db.get_all(
#                 "Job Card",
#                 filters=filters,
#                 fields=["name"],
#             )
            
#             # Fetching the employee from the child table based on the Job Cards
#             job_card_employees = frappe.db.get_all(
#                 "Job Card Time Log",  # Assuming the child table is "Job Card Time Log"
#                 filters={"parent": ["in", [job["name"] for job in job_cards]]},
#                 fields=["parent", "employee"]
#             )

#             # Create a dictionary to associate Job Card with Employees
#             job_card_employee_map = {}
#             for entry in job_card_employees:
#                 if entry["parent"] not in job_card_employee_map:
#                     job_card_employee_map[entry["parent"]] = []
#                 job_card_employee_map[entry["parent"]].append(entry["employee"])
            
#             # Fetch the user_id for each employee
#             job_card_user_map = {}
#             for job_card, employees in job_card_employee_map.items():
#                 job_card_user_map[job_card] = []
#                 for employee in employees:
#                     user_id = frappe.db.get_value('Employee', employee, 'user_id')
#                     job_card_user_map[job_card].append({
#                         "employee": employee,
#                         "user_id": user_id
#                     })
            
#             # Combine the job cards with the associated employees and their user_ids
#             result = []
#             for job in job_cards:
#                 result.append({
#                     "job_card": job["name"],
#                     "employees": job_card_user_map.get(job["name"], [])
#                 })
            
#             return result
        
#         except QueryDeadlockError:
#             retries += 1
#             if retries < max_retries:
#                 frappe.msgprint(f"Deadlock detected. Retrying ({retries}/{max_retries})...")
#                 time.sleep(2)  # Add a short delay before retrying
#             else:
#                 frappe.throw("Deadlock error occurred. Retry limit reached.")