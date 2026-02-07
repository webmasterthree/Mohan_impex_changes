// Copyright (c) 2025, Edubild and contributors
// For license information, please see license.txt

frappe.ui.form.on('Journey Plan', {
    setup(frm) {
        // Warm both caches early
        preload_primary_customers();
    },
    refresh(frm) {
        // Ensure caches are ready, then bind focus handlers once
        Promise.all([preload_primary_customers()]).then(() => {
            bind_primary_focus_handler(frm);
        });
    },
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


// ---- Journey Plan: Primary & Secondary customer multi-select-to-CSV for trips child table ----

// Caches & bind flags
let __PRIMARY_CACHE = [];
let __PRIMARY_BIND_DONE = false;

// Get value from mohans_impex/api/auth.py
function has_cp() {
    return new Promise((resolve, reject) => {
        frappe.call({
            method: 'mohan_impex.api.auth.has_cp',
            callback: (r) => {
                return resolve(r.message);
            }
        });
    });
}
// Load once and cache the list of Primary customers
function preload_primary_customers() {
    if (__PRIMARY_CACHE.length) return Promise.resolve(__PRIMARY_CACHE);
    filters = {}
    if (has_cp()) {
        filters = { customer_level: 'Primary' }
    }
    return new Promise((resolve) => {
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Customer',
                filters: filters,
                fields: ['name'],
                order_by: 'name asc',
                limit_page_length: 1000
            },
            callback: (r) => {
                __PRIMARY_CACHE = (r.message || []).map(d => d.name);
                resolve(__PRIMARY_CACHE);
            },
            error: () => resolve([])
        });
    });
}

// Normalize MultiCheck return formats across Frappe versions
function normalize_multicheck(val) {
    if (Array.isArray(val)) {
        // Could be array of strings or array of {label,value,checked}
        return val
            .map(v => (typeof v === 'string' ? v : (v?.value || v?.label || '')))
            .filter(Boolean);
    }
    if (val && typeof val === 'object') {
        // Could be object map: { "Customer A": 1, "Customer B": 0 }
        return Object.keys(val).filter(k => !!val[k]);
    }
    return [];
}

// Generic picker dialog for a given field + option list
function open_customer_picker_dialog({ frm, cdt, cdn, fieldname, title, options_source }) {
    const row = locals[cdt][cdn];
    if (!row) return;

    const choices = options_source();
    if (!choices.length) {
        frappe.msgprint(__('No customers found for {0}.', [title]));
        return;
    }

    const already = (row[fieldname] || '')
        .split(',')
        .map(s => s.trim())
        .filter(Boolean);

    const options = choices.map(name => ({
        label: name,
        value: name,
        checked: already.includes(name)
    }));

    const d = new frappe.ui.Dialog({
        title,
        size: 'large',
        fields: [
            {
                fieldname: 'customers',
                fieldtype: 'MultiCheck',
                label: title,
                options
            }
        ],
        primary_action_label: __('Apply'),
        primary_action(values) {
            const chosen = normalize_multicheck(values.customers);
            const unique = [...new Set(chosen)].map(s => s.trim()).filter(Boolean);
            row[fieldname] = unique.join(', ');
            d.hide();
            frm.refresh_field('trips');
        }
    });

    d.show();
}

// ---- Primary Customer: focus binding ----
function bind_primary_focus_handler(frm) {
    const grid = frm.fields_dict?.trips?.grid;
    if (!grid || __PRIMARY_BIND_DONE) return;

    $(grid.wrapper).on(
        'focus',
        'input[data-fieldname="primary_customer"], textarea[data-fieldname="primary_customer"]',
        function (e) {
            const $row = $(this).closest('.grid-row');
            const cdn = $row.attr('data-name');
            const cdt = grid.doctype;
            if (!cdn || !cdt) return;

            e.preventDefault();
            $(this).blur();

            open_customer_picker_dialog({
                frm, cdt, cdn,
                fieldname: 'primary_customer',
                title: __('Select Primary Customers'),
                options_source: () => __PRIMARY_CACHE
            });
        }
    );

    __PRIMARY_BIND_DONE = true;
}