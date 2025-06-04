import frappe
from mohan_impex.mohan_impex.comment import workflow_status_update

@frappe.whitelist()
def get_trial_template(item_code):
    trial_template = frappe.get_all("Trial Template Table", {"parent": item_code}, ["trial_parameter", "type", "is_need_remarks"])
    frappe.local.response['status'] = True
    frappe.local.response['data'] = trial_template

@frappe.whitelist()
def get_trial_target(trial_target):
    if not trial_target:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = "Please select the Trial Target"
        return
    if not frappe.db.exists("Trial Target", trial_target):
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = "Please select the valid Trial Target"
        return
    trial_target = frappe.get_doc("Trial Target", {"name": trial_target}, ["*"])
    trial_target = trial_target.as_dict()
    fields_to_remove = ["owner", "creation", "modified", "modified_by", "docstatus", "idx", "amended_from", "doctype", "parent", "parenttype", "parentfield"]
    child_doc = ["trial_target_table"]
    trial_target = {
        key: value for key, value in trial_target.items() if key not in fields_to_remove
    }
    for child_name in child_doc:
        if child_name in trial_target:
            trial_target[child_name] = [
                {k: v for k, v in item.items() if k not in fields_to_remove}
                for item in trial_target[child_name]
            ]
    trial_target["item_name"] = frappe.get_value("Item", trial_target.get("item_code"), "item_name")
    # trial_target["comp_item_name"] = frappe.get_value("Item", trial_target.get("comp_item"), "item_name") if trial_target.get("comp_item") else ""
    trial_target["parameters"] = trial_target.pop("trial_target_table")
    frappe.local.response['status'] = True
    frappe.local.response['data'] = trial_target

@frappe.whitelist()
def update_trial_target():
    try:
        trial_plan_table_dict = frappe.form_dict
        # trial_plan_id = trial_plan_table_dict.get("trial_plan")
        trial_target = trial_plan_table_dict.get("trial_target")
        trial_target_doc = frappe.get_doc("Trial Target", trial_target)
        parameters = trial_plan_table_dict.get("parameters")
        trial_row_fields = [
            "batch_no", "mfg_date", "batch_size", "batch_uom", "no_of_batches", "has_competitor", "competitor_brand", "comp_brand_remarks", "current_dosage", "dosage_uom", "reason_for_competition", "competition_remarks", "reason",
            "reason_remarks", "mon_cons", "mon_cons_uom", "is_order_recieved", "ord_nrc_reason", "comp_item", "comp_item_remarks",
            "demo_result", "next_expec_order_date", "ord_nrc_remarks"
        ]
        for field in trial_row_fields:
            setattr(trial_target_doc, field, trial_plan_table_dict.get(field))
        trial_target_doc.save()

        trial_target_table = frappe.get_all("Trial Target Table", {"parent": trial_target}, ["*"])
        for trial_target_row in trial_target_table:
            trial_target_row_doc = frappe.get_doc("Trial Target Table", trial_target_row.name)
            for parameter in parameters:
                if parameter.get("trial_parameter") == trial_target_row_doc.trial_parameter:
                    if parameter.get("type") == "Satisfaction Status":
                        trial_target_row_doc.satisfaction_status = parameter.get("satisfaction_status")
                    elif parameter.get("type") == "Minutes":
                        trial_target_row_doc.minutes = parameter.get("minutes")
                    elif parameter.get("type") == "Temperature":
                        trial_target_row_doc.temperature = parameter.get("temperature")
                    trial_target_row_doc.remarks = parameter.get("remarks")
                    trial_target_row_doc.save()
                    break
        frappe.local.response['status'] = True
        frappe.local.response['message'] = "Trial Target Updated Successfully"
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"

@frappe.whitelist()
def complete_trial_target():
    try:
        trial_target_id = frappe.form_dict.get("trial_target_id")
        if not trial_target_id:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Please select the Trial Target"
            return
        if not frappe.db.exists("Trial Target", trial_target_id):
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = "Please select the valid Trial Target"
            return
        trial_target_doc = frappe.get_doc("Trial Target", trial_target_id)
        invalid_err_msg = trial_target_doc.validate_trial()
        if invalid_err_msg:
            frappe.local.response['http_status_code'] = 404
            frappe.local.response['status'] = False
            frappe.local.response['message'] = invalid_err_msg
            return
        trial_target_doc.status = "Completed"
        response = workflow_status_update("Trial Target", trial_target_id, "Draft")
        return response
    except Exception as err:
        frappe.local.response['http_status_code'] = 404
        frappe.local.response['status'] = False
        frappe.local.response['message'] = frappe.local.response.get('message') or f"{err}"
