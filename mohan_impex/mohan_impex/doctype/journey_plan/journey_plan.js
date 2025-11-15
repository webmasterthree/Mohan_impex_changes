// Copyright (c) 2025, Edubild and contributors
// For license information, please see license.txt

frappe.ui.form.on('Journey Plan', {
    setup(frm) {
        // Warm both caches early
        preload_primary_customers();
        preload_secondary_customers();
    },
    refresh(frm) {
        // Ensure caches are ready, then bind focus handlers once
        Promise.all([preload_primary_customers(), preload_secondary_customers()]).then(() => {
            bind_primary_focus_handler(frm);
            bind_secondary_focus_handler(frm);
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
let __SECONDARY_CACHE = [];
let __PRIMARY_BIND_DONE = false;
let __SECONDARY_BIND_DONE = false;

// Load once and cache the list of Primary customers
function preload_primary_customers() {
    if (__PRIMARY_CACHE.length) return Promise.resolve(__PRIMARY_CACHE);

    return new Promise((resolve) => {
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Customer',
                filters: { customer_level: 'Primary' },
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

// Load once and cache the list of Secondary customers
function preload_secondary_customers() {
    if (__SECONDARY_CACHE.length) return Promise.resolve(__SECONDARY_CACHE);

    return new Promise((resolve) => {
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Customer',
                filters: { customer_level: 'Secondary' },
                fields: ['name'],
                order_by: 'name asc',
                limit_page_length: 1000
            },
            callback: (r) => {
                __SECONDARY_CACHE = (r.message || []).map(d => d.name);
                resolve(__SECONDARY_CACHE);
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

// ---- Secondary Customer: focus binding ----
function bind_secondary_focus_handler(frm) {
    const grid = frm.fields_dict?.trips?.grid;
    if (!grid || __SECONDARY_BIND_DONE) return;

    $(grid.wrapper).on(
        'focus',
        'input[data-fieldname="secondary_customer"], textarea[data-fieldname="secondary_customer"]',
        function (e) {
            const $row = $(this).closest('.grid-row');
            const cdn = $row.attr('data-name');
            const cdt = grid.doctype;
            if (!cdn || !cdt) return;

            e.preventDefault();
            $(this).blur();

            open_customer_picker_dialog({
                frm, cdt, cdn,
                fieldname: 'secondary_customer',
                title: __('Select Secondary Customers'),
                options_source: () => __SECONDARY_CACHE
            });
        }
    );

    __SECONDARY_BIND_DONE = true;
}