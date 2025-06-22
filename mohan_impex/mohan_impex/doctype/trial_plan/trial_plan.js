// Copyright (c) 2025, Edubild and contributors
// For license information, please see license.txt

frappe.ui.form.on("Trial Plan", {
  async refresh(frm) {
    assigned_to_employee(frm)
    if (frm.is_new()){
      frm.set_value("channel_partner", "");
    }
  },
  after_workflow_action(frm){
    if (frm.doc.status === "Approved"){
      frappe.db.set_value("Trial Plan", frm.doc.name, 'approved_date', frappe.datetime.nowdate())
    }
    else if (frm.doc.status === "Rejected"){
      frappe.db.set_value("Trial Plan", frm.doc.name, 'rejected_date', frappe.datetime.nowdate())
    }
  },
  conduct_by(frm){
    if (frm.doc.conduct_by === "TSM Required"){
      frm.set_value("assigned_to", "")
    }
    else{
      frm.set_value("assigned_to", frm.doc.created_by_emp)
    }
  },
  customer_level(frm){
    frm.set_value("customer", "")
    frm.set_value("unv_customer", "")
  },
  verific_type(frm){
    frm.set_value("customer", "")
    frm.set_value("unv_customer", "")
  },
  customer(frm) {
    if (frm.doc.customer) {
      frm.call("get_contact_and_address").then((r) => {
        if (r.message) {
          let response = r.message;
          // frm.set_value("contact", response.contact);
          frm.set_value("location", response.address);
        }
      });
    }
  },
  customer(frm) {
    if (frm.doc.customer) {
      set_customer_info(frm)
    }
    else{
      frm.set_value("shop", "");
      frm.set_value("channel_partner", "");
      frm.set_value("contact", []);
      frm.set_value("location", "");
    }
  },
  unv_customer(frm) {
    if (frm.doc.unv_customer) {
      set_customer_info(frm)
    }
    else{
      frm.set_value("shop", "");
      frm.set_value("channel_partner", "");
      frm.set_value("contact", []);
      frm.set_value("location", "");
    }
  },
	onload(frm) {
    if (frm.is_new()) {
        set_session_employee(frm)
    }
  },
  before_save(frm) {
      set_session_employee(frm)
  },
});

cur_frm.set_query("customer", function (frm) {
  var filter_dict = {
    customer_level: cur_frm.doc.customer_level,
  }
  if (cur_frm.doc.channel_partner){
    filter_dict.custom_channel_partner = cur_frm.doc.channel_partner
  }
  return {
    filters: filter_dict,
  };
});

cur_frm.set_query("unv_customer", function (frm) {
  var filter_dict = {
    customer_level: cur_frm.doc.customer_level,
  }
  if (cur_frm.doc.channel_partner){
    filter_dict.channel_partner = cur_frm.doc.channel_partner
  }
  return {
    filters: filter_dict,
  };
});

cur_frm.set_query("contact", function async (frm) {
  let contact_list = []
  frappe.call({
    method: "mohan_impex.config.get_contacts",
    args: {
      "verific_type": cur_frm.doc.verific_type,
      "customer": cur_frm.doc.customer,
      "unv_customer": cur_frm.doc.unv_customer
    },
    async: false,
    callback(r){
      contact_list = r.message
    }
  })
  return {
    filters: [["name", "in", contact_list]]
  };
});

cur_frm.set_query("location", function async (frm) {
  let address_list = []
  frappe.call({
    method: "mohan_impex.config.get_addresses",
    args: {
      "verific_type": cur_frm.doc.verific_type,
      "customer": cur_frm.doc.customer,
      "unv_customer": cur_frm.doc.unv_customer
    },
    async: false,
    callback(r){
      address_list = r.message
    }
  })
  return {
    filters: [["name", "in", address_list]]
  };
});

cur_frm.set_query("item_code", "trial_plan_table", function (frm, cdt, cdn) {
  var row = locals[cdt][cdn];
  var product_items = []
  var args = {
    "product" : row.product
  }
  console.log("r.message")
  frappe.call({
      method: "mohan_impex.mohan_impex.doctype.customer_visit_management.customer_visit_management.get_product_items",
      args: args,
      async: false,
      callback(r){
        console.log(r.message)
        product_items = r.message
      }
  })

  return {
    filters: [
      ["has_variants", "=", 1],
      ["name", "in", product_items]
    ],
  };
});

function set_customer_info(frm){
  frm.call("get_contact_and_address").then((r) => {
    if (r.message) {
      let response = r.message;
      console.log([response, "response"])
      if(response){
        frm.set_value("shop", response.shop);
        frm.set_value("channel_partner", response.channel_partner);
        frm.set_value("contact", response.contact);
        frm.set_value("location", response.address);
      }
    }
  });
}

function set_session_employee(frm){
  if(!frm.doc.created_by_emp){
    frappe.call({
      method: "mohan_impex.mohan_impex.utils.get_session_employee",
      async:false,
      callback: function (r) {
        if (r.message) {
          console.log(r.message)
          frm.set_value("created_by_emp", r.message);
          frm.refresh_field("created_by_emp")
        }
      }
    });
  }
}

function assigned_to_employee(frm){
  frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "role_profile").then((r) => {
    if (frm.doc.conduct_by === "TSM Required" && frm.doc.status !== "Rejected" && (r.message.role_profile === "NSM" || frappe.session.user === "Administrator")){
      frm.add_custom_button(__('Assign Employee'), function() {
        var d = new frappe.ui.Dialog({
          title: __("Select Employee"),
          fields: [
            {
              fieldtype: "Link",
              label: __("Assign To"),
              options: "Employee",
              fieldname: "employee",
              reqd: 1,
              default: frm.doc.assigned_to,
              get_query() {
                return {
                  filters: {
                    "role_profile": "TSM"
                  }
                }
              }
            }
          ],
          primary_action: function() {
            frm.set_value("assigned_to", d.fields_dict.employee.get_value());
            frm.save();
            d.hide();
          }
        });
        d.show();
      });
    }
  })
}

// cur_frm.set_query("product", "product_pitching", function (frm, cdt, cdn) {
//   var row = locals[cdt][cdn];
//   return {
//     filters: [["item_group", "=", row.product_type]],
//   };
// });
