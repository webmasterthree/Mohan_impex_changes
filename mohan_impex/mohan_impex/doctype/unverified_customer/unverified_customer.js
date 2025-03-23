// Copyright (c) 2025, Edubild and contributors
// For license information, please see license.txt

frappe.ui.form.on("Unverified Customer", {
	refresh(frm){
    if(frm.doc.kyc_status === "Pending"){
      frm.add_custom_button(__("Create Customer"), () => {
        create_customer(frm)
      })
    }
  },
  before_save(frm) {
    set_session_employee(frm)
	}
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

  function create_customer(frm){
    frappe.model.with_doctype('Customer', function() {
      let cu = frappe.model.get_new_doc('Customer');
      cu.unv_customer = frm.doc.name
      frappe.set_route('Form', 'Customer', cu.name);
    })
  }