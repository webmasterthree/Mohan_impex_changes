// Copyright (c) 2025, Edubild and contributors
// For license information, please see license.txt

frappe.ui.form.on("Customer Visit Management", {
  async refresh(frm) {
    let kyc_status = false
    let customer_url = ""
    // console.log(frm.doc.customer_level)
    // if (frm.doc.customer_level === "Primary" ){
      await frm.call("get_kyc_status").then((r) => {
        if (r.message) {
          kyc_status = r.message.kyc_status
          customer_url = r.message.customer_url
        }
      });
    // }
    if (frm.doc.docstatus === 1) {
      if(kyc_status){
        frm.add_custom_button(__("Create Sales Order"), () => {
          create_sales_order(frm)
        })
      }
      else{
        frm.add_custom_button(__("Complete KYC"), () => {
          window.open(customer_url, "_blank");
        });
      }
    }
  },
  onload(frm) {
    if (frm.is_new() && !frm.doc.visit_start) {
      const now = new Date();
      frm.set_value("visit_start", convertToDateTime(now));
      // set_session_employee(frm)
      set_current_map_location(frm);
    }
  },
  verific_type(frm){
    frm.set_value("customer", "")
    frm.set_value("unv_customer", "")
  },
  customer_type(frm){
    if(frm.doc.customer_type === "New"){
      frm.set_value("verific_type", "Unverified")
    }
  },
  customer(frm) {
    if (!frm.doc.customer) {
      frm.set_value("shop", "");
      frm.set_value("contact", []);
      frm.set_value("location", "");
    }
    else{
      set_customer_info(frm)
    }
  },
  unv_customer(frm) {
    if (!frm.doc.unv_customer) {
      frm.set_value("shop", "");
      frm.set_value("contact", []);
      frm.set_value("location", "");
    }
    else{
      set_customer_info(frm)
    }
  },
  before_save(frm) {
    const now = new Date();
    frm.set_value("visit_end", convertToDateTime(now));
    const visit_start = new Date(frm.doc.visit_start);
    const visit_end = new Date(frm.doc.visit_end);
    const differenceInSeconds = Math.floor((visit_end - visit_start) / 1000);
    frm.set_value("visit_duration", differenceInSeconds);
    // set_session_employee(frm)
  },
  after_save(frm){
    frm.call("trial_plan")
  }
});

function set_customer_info(frm){
  frm.call("get_contact_and_address").then((r) => {
    if (r.message) {
      let response = r.message;
      console.log(response)
      if(response){
        frm.set_value("shop", response.shop);
        frm.set_value("contact", response.contact);
        frm.set_value("location", response.address);
      }
    }
  });
}

function convertToDateTime(jsDate) {
  const year = jsDate.getFullYear();
  const month = String(jsDate.getMonth() + 1).padStart(2, "0"); // Months are 0-based
  const day = String(jsDate.getDate()).padStart(2, "0");
  const hours = String(jsDate.getHours()).padStart(2, "0");
  const minutes = String(jsDate.getMinutes()).padStart(2, "0");
  const seconds = String(jsDate.getSeconds()).padStart(2, "0");

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

function set_current_map_location(frm) {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        const map_location = JSON.stringify({
          type: "FeatureCollection",
          features: [
            {
              type: "Feature",
              properties: {},
              geometry: { type: "Point", coordinates: [longitude, latitude] },
            },
          ],
        });
        frm.set_value("map_location", map_location);
      },
      (error) => {
        console.error(`Error Code: ${error.code}, Message: ${error.message}`);
      }
    );
  } else {
    console.log("Geolocation is not supported by this browser.");
  }
}

cur_frm.set_query("customer", function (frm) {
  var filter_dict = {}
  if (cur_frm.doc.channel_partner){
    filter_dict.custom_channel_partner = cur_frm.doc.channel_partner
  }
  return {
    filters: filter_dict,
  };
});

cur_frm.set_query("unv_customer", function (frm) {
  var filter_dict = {}
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

cur_frm.set_query("item_code", "product_pitching", function (frm, cdt, cdn) {
  var row = locals[cdt][cdn];
  var product_items = []
  var args = {
    "segment" : row.segment
  }
  console.log("r.message")
  frappe.call({
      method: "mohan_impex.mohan_impex.doctype.customer_visit_management.customer_visit_management.get_product_items",
      args: args,
      async: false,
      callback(r){
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

frappe.ui.form.on("Product Pitching", {
  product_pitching_add(frm, cdt, cdn) {
    var row = frappe.get_doc(cdt, cdn);
    prdct_pitch_len = frm.doc.product_pitching.length;
    const prev_row = frm.doc.product_pitching[prdct_pitch_len - 2];
    if (prev_row) {
      row.product_type = prev_row.product_type;
    }
    frm.refresh_field("product_pitching");
  },
  segment(frm, cdt, cdn) {
    var row = locals[cdt][cdn];
    row.qty = row.segment ? 1 : 0;
    row.item_code=""
    frm.refresh_field("product_pitching");
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

function create_sales_order(frm){
  frappe.model.with_doctype('Sales Order', function() {
    let so = frappe.model.get_new_doc('Sales Order');
    so.customer = frm.doc.customer;
    so.customer_level = frm.doc.customer_level;
    so.custom_channel_partner = frm.doc.channel_partner;
    so.custom_deal_type = frm.doc.deal_type;
    so.transaction_date = frappe.datetime.nowdate();
    so.customer_visit = frm.doc.name
    so.shop = frm.doc.shop;

    // Initialize items array properly
    so.items = [];

    // Add an item ensuring required fields are present
    frm.doc.product_pitching.forEach(pitch => {
      let child = frappe.model.add_child(so, "items");
      child.item_template = pitch.item_code; // Fallback if undefined
      child.item_category = pitch.item_category;
      child.qty = pitch.qty || 1;
    });
    frappe.set_route('Form', 'Sales Order', so.name);
  })
}