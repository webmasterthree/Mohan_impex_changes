// Copyright (c) 2025, Edubild and contributors
// For license information, please see license.txt

frappe.ui.form.on("Trial Plan", {
  async refresh(frm) {
    if (frm.is_new()){
      frm.set_value("channel_partner", "");
    }
  },
  after_workflow_action(frm){
    if (frm.doc.status === "Approved"){
      frappe.db.set_value("Trial Plan", frm.doc.name, 'approved_date', frappe.datetime.nowdate())
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

function set_customer_info(frm){
  frm.call("get_contact_and_address").then((r) => {
    if (r.message) {
      let response = r.message;
      console.log(response)
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
          frm.set_value("created_by_emp", r.message);
          frm.refresh_field("created_by_emp")
        }
      }
    });
  }
}

// cur_frm.set_query("product", "product_pitching", function (frm, cdt, cdn) {
//   var row = locals[cdt][cdn];
//   return {
//     filters: [["item_group", "=", row.product_type]],
//   };
// });
