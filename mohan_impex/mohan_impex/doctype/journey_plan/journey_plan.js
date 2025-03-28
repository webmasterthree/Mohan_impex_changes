// Copyright (c) 2025, Edubild and contributors
// For license information, please see license.txt

frappe.ui.form.on("Journey Plan", {
	onload(frm) {
    if (frm.is_new()) {
      set_session_employee(frm)
    }
  },
  after_workflow_action(frm){
    if (frm.doc.status === "Approved"){
      frappe.db.set_value("Journey Plan", frm.doc.name, 'approved_date', frappe.datetime.nowdate())
    }
    else if (frm.doc.status === "Rejected"){
      frappe.db.set_value("Journey Plan", frm.doc.name, 'rejected_date', frappe.datetime.nowdate())
    }
  },
  before_save(frm) {
    set_session_employee(frm)
  },
});

function set_session_employee(frm){
  if(!frm.doc.created_by_emp){
    frappe.call({
      method: "mohan_impex.mohan_impex.utils.get_session_employee",
      async:false,
      callback: function (r) {
        if (r.message) {
          frm.set_value("created_by_emp", r.message);
          frm.refresh_field("created_by_emp")
        }
      }
    });
  }
}