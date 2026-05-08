frappe.ui.form.on('Purchase Receipt', {
    validate: async function (frm) {
        update_pre_unloading_status(frm);
        calculate_labour_cost(frm);
        await check_shelf_and_set(frm);
    },

    custom_labour_rate_per_ton: function (frm) {
        calculate_labour_cost(frm);
    },

    custom_total_weight: function (frm) {
        calculate_labour_cost(frm);
    },

    custom_no_of_labour: function (frm) {
        calculate_labour_cost(frm);
    },

    custom_labour_rate: function (frm) {
        calculate_labour_cost(frm);
    },

    onload: function (frm) {
        set_batch_query_filter(frm);
    },

    after_save(frm) {
        fetch_po_fields_and_set_on_pr(frm);
    },

    miscellaneous_expenses_remove(frm) {
        update_total_misc_amount(frm);
    },

    refresh: function (frm) {
        if (frappe.session.user == "Administrator" || frm.doc.docstatus == 0) {
            frm.add_custom_button("Check Expired Batches", function () {
                calculate_accept_reject(frm);
            });
        }

        if (frm.doc.workflow_state == "Purchase Team Approval Pending") {
            frm.page.clear_actions_menu();

            frm.page.set_primary_action('Review', () => {
                calculate_accept_reject1(frm);
            });
        }
    },

    before_workflow_action: async function (frm) {
        if (frm.doc.workflow_state === "Complete GRN") {
            await calculate_accept_reject(frm);
        }
    }
});


frappe.ui.form.on('Purchase Receipt Item', {
    custom_manufacturing_date: function (frm, cdt, cdn) {
        calculate_remaining_shelf_life(frm, cdt, cdn);
    },

    custom_shelf_life_in_days: function (frm, cdt, cdn) {
        frappe.ui.form.trigger(cdt, cdn, 'custom_manufacturing_date');
    }
});


function calculate_remaining_shelf_life(frm, cdt, cdn) {
    let row = locals[cdt][cdn];

    if (row.custom_manufacturing_date && row.custom_shelf_life_in_days) {
        let mfg_date = frappe.datetime.str_to_obj(row.custom_manufacturing_date);
        let today = frappe.datetime.str_to_obj(frappe.datetime.now_date());

        let days_since_mfg = frappe.datetime.get_day_diff(today, mfg_date);
        let remaining_life = row.custom_shelf_life_in_days - days_since_mfg;

        frappe.model.set_value(cdt, cdn, 'custom_remaining_shelf_life', remaining_life);

        if (remaining_life > 0) {
            frappe.model.set_value(cdt, cdn, 'custom_purchase_team_approval', 'Approved');
        } else {
            frappe.model.set_value(cdt, cdn, 'custom_purchase_team_approval', 'Pending');

            frappe.msgprint({
                title: __('Warning'),
                message: __('This item has expired! Purchase Team Approval is required.'),
                indicator: 'red'
            });
        }
    }

    update_pre_unloading_status(frm);
}


function update_pre_unloading_status(frm) {
    let total_weight = (frm.doc.items || []).reduce((sum, item) => {
        let qty = flt(item.qty) + flt(item.rejected_qty);
        let factor = flt(item.conversion_factor || 1);
        return sum + (qty * factor);
    }, 0);

    frm.set_value('custom_total_weight', total_weight);
    frm.refresh_fields(['custom_total_weight']);
}


function calculate_labour_cost(frm) {
    let total_weight = flt(frm.doc.custom_total_weight || 0);
    let labour_rate = flt(frm.doc.custom_labour_rate || 0);
    let factor = flt(frm.doc.conversion_factor || 1);
    let additional_cost = flt(frm.doc.additional_cost || 0);

    let total_cost = 0;

    if (total_weight && labour_rate) {
        total_cost = (total_weight * labour_rate) / factor + additional_cost;
    }

    if (total_cost === 0) {
        let no_of_labour = flt(frm.doc.custom_no_of_labour || 0);
        let rate_per_ton = flt(frm.doc.custom_labour_rate_per_ton || 0);

        if (no_of_labour && rate_per_ton && total_weight) {
            total_cost = (no_of_labour * rate_per_ton * total_weight) / 1000;
        }
    }

    frm.set_value('custom_total_labour_cost', total_cost);
}


function set_batch_query_filter(frm) {
    frm.fields_dict.items.grid.get_field('batch_no').get_query = function (doc, cdt, cdn) {
        const row = locals[cdt][cdn];

        let filters = {
            item: row.item_code
        };

        if (row.custom_select_brand) {
            filters.custom_brand = row.custom_select_brand;
        }

        return { filters };
    };
}


function fetch_po_fields_and_set_on_pr(frm) {
    if (!frm.doc.items || frm.doc.items.length === 0) {
        return;
    }

    const po_in_item = frm.doc.items[0].purchase_order;

    if (!po_in_item) {
        return;
    }

    frappe.call({
        method: "mohan_impex.PR_Connection.get_linked_purchase_order",
        args: {
            purchase_receipt: frm.doc.name
        },
        callback: function (r) {
            if (!r.message) {
                return;
            }

            if (r.message.status === "error") {
                frappe.msgprint(
                    __("Error fetching Purchase Order details: {0}", [r.message.message])
                );
                return;
            }

            const data = r.message;

            frm.set_value("custom_transporters_name", data.custom_transporter_name || "");
            frm.set_value("custom_vehicle_no__container_no", data.custom_vehiclecontainer_number || "");
            frm.set_value("assigned_driver", data.custom_driver_name || "");
            frm.set_value("driver_mobile_number", data.custom_driver_mobile_number || "");
            frm.set_value("lr_number", data.lr_no || "");
        }
    });
}


frappe.ui.form.on("Miscellaneous Expense Items", {
    qty(frm, cdt, cdn) {
        update_item_amount_and_total(frm, cdt, cdn);
    },

    rate(frm, cdt, cdn) {
        update_item_amount_and_total(frm, cdt, cdn);
    },
});


function update_item_amount_and_total(frm, cdt, cdn) {
    const row = locals[cdt][cdn];

    const qty = flt(row.qty) || 0;
    const rate = flt(row.rate) || 0;
    const amt_precision = typeof precision === "function" ? precision("amount", row) : 2;

    const amount = flt(qty * rate, amt_precision);

    frappe.model.set_value(cdt, cdn, "amount", amount);

    update_total_misc_amount(frm, amt_precision);
}


function update_total_misc_amount(frm, amt_precision) {
    const precision_to_use =
        typeof precision === "function"
            ? precision("total_misc_amount", frm.doc)
            : (amt_precision || 2);

    let total = 0;

    (frm.doc.miscellaneous_expenses || []).forEach((d) => {
        total += flt(d.amount) || 0;
    });

    frm.set_value("total_misc_amount", flt(total, precision_to_use));
    frm.refresh_field("total_misc_amount");
}


// ========================================================
// BACKEND API CALL FOR REMAINING SHELF LIFE
// ========================================================

async function get_remaining_shelf_life(batch_no) {
    if (!batch_no) {
        return 0;
    }

    try {
        let r = await frappe.call({
            method: "mohan_impex.shelf_life.remaining_shelf_life",
            args: {
                batch: batch_no
            }
        });

        return flt(r.message || 0);

    } catch (e) {
        console.error("Remaining shelf life API error for batch:", batch_no, e);
        return 0;
    }
}


// ========================================================
// GET SHELF LIFE DAYS FROM ITEM
// ========================================================

async function get_item_shelf_life_days(item_code) {
    if (!item_code) {
        return 0;
    }

    try {
        let r = await frappe.db.get_value("Item", item_code, "shelf_life_in_days");
        return flt(r?.message?.shelf_life_in_days || 0);

    } catch (e) {
        console.error("Item shelf life fetch error:", item_code, e);
        return 0;
    }
}


// ========================================================
// DATE FORMATTER - dd-mm-yyyy
// ========================================================

function format_date_dd_mm_yyyy(date_value) {
    if (!date_value) {
        return "";
    }

    try {
        let date_obj;

        if (typeof date_value === "string") {
            date_obj = frappe.datetime.str_to_obj(date_value);
        } else {
            date_obj = date_value;
        }

        if (!date_obj) {
            return date_value;
        }

        let day = String(date_obj.getDate()).padStart(2, "0");
        let month = String(date_obj.getMonth() + 1).padStart(2, "0");
        let year = date_obj.getFullYear();

        return `${day}-${month}-${year}`;

    } catch (e) {
        return date_value;
    }
}


// ========================================================
// TOOLTIP FORMATTER
// ========================================================

function make_batch_tooltip(batch_rows) {
    if (!batch_rows || batch_rows.length === 0) {
        return "No batch found";
    }

    return batch_rows.map(row => {
        return [
            `Batch: ${row.batch_no || ""}`,
            `Qty: ${row.qty || 0}`,
            row.expiry_date ? `Expiry: ${format_date_dd_mm_yyyy(row.expiry_date)}` : null,
            row.remaining_shelf_life !== undefined ? `Remaining: ${row.remaining_shelf_life} days` : null,
            row.percent !== undefined ? `Shelf Life: ${row.percent}%` : null
        ].filter(Boolean).join(" | ");
    }).join("\n");
}


// ========================================================
// CUSTOM COLORED BOOTSTRAP TOOLTIP ONLY
// NO COLOR IN DIALOG TABLE CELL
// ========================================================

function apply_batch_hover_tooltips(dialog) {
    setTimeout(() => {
        if (!dialog || !dialog.fields_dict || !dialog.fields_dict.items) {
            return;
        }

        // Add CSS only once
        if (!document.getElementById("batch-tooltip-style")) {
            $("head").append(`
                <style id="batch-tooltip-style">
                    .batch-tooltip-lt25 .tooltip-inner {
                        background-color: #fff3cd !important;
                        color: #856404 !important;
                        border: 1px solid #ffeeba !important;
                        max-width: 520px !important;
                        text-align: left !important;
                        white-space: pre-line !important;
                        font-weight: 600 !important;
                        padding: 10px 12px !important;
                        border-radius: 6px !important;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
                    }

                    .batch-tooltip-gt25 .tooltip-inner {
                        background-color: #d4edda !important;
                        color: #155724 !important;
                        border: 1px solid #c3e6cb !important;
                        max-width: 520px !important;
                        text-align: left !important;
                        white-space: pre-line !important;
                        font-weight: 600 !important;
                        padding: 10px 12px !important;
                        border-radius: 6px !important;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
                    }

                    .batch-tooltip-expiry .tooltip-inner {
                        background-color: #f8d7da !important;
                        color: #721c24 !important;
                        border: 1px solid #f5c6cb !important;
                        max-width: 520px !important;
                        text-align: left !important;
                        white-space: pre-line !important;
                        font-weight: 600 !important;
                        padding: 10px 12px !important;
                        border-radius: 6px !important;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
                    }

                    .batch-tooltip-lt25.bs-tooltip-top .arrow::before,
                    .batch-tooltip-lt25.bs-tooltip-auto[x-placement^="top"] .arrow::before {
                        border-top-color: #fff3cd !important;
                    }

                    .batch-tooltip-gt25.bs-tooltip-top .arrow::before,
                    .batch-tooltip-gt25.bs-tooltip-auto[x-placement^="top"] .arrow::before {
                        border-top-color: #d4edda !important;
                    }

                    .batch-tooltip-expiry.bs-tooltip-top .arrow::before,
                    .batch-tooltip-expiry.bs-tooltip-auto[x-placement^="top"] .arrow::before {
                        border-top-color: #f8d7da !important;
                    }

                    .batch-tooltip-hover-target {
                        cursor: help !important;
                    }
                </style>
            `);
        }

        let grid = dialog.fields_dict.items.grid;

        if (!grid || !grid.grid_rows) {
            return;
        }

        function set_custom_tooltip($target, text, tooltip_class) {
            if (!$target || !$target.length) {
                return;
            }

            $target.each(function () {
                let $el = $(this);

                // Remove browser default tooltip
                $el.removeAttr("title");

                // Remove old tooltip instance if any
                try {
                    $el.tooltip("dispose");
                } catch (e) {}

                // Remove any old color classes if previous script added them
                $el.removeClass("batch-cell-lt25 batch-cell-gt25 batch-cell-expiry");

                // Remove inline color/background/font styles from earlier version
                $el.css({
                    "background-color": "",
                    "color": "",
                    "font-weight": ""
                });

                $el
                    .addClass("batch-tooltip-hover-target")
                    .attr("data-toggle", "tooltip")
                    .attr("data-placement", "top")
                    .attr("data-html", "false")
                    .attr("data-container", "body")
                    .attr("data-original-title", text);

                try {
                    $el.tooltip({
                        container: "body",
                        placement: "top",
                        html: false,
                        trigger: "hover",
                        template: `
                            <div class="tooltip ${tooltip_class}" role="tooltip">
                                <div class="arrow"></div>
                                <div class="tooltip-inner"></div>
                            </div>
                        `
                    });
                } catch (e) {
                    // Fallback if Bootstrap tooltip is not available
                    $el.attr("title", text);
                }
            });
        }

        grid.grid_rows.forEach(grid_row => {
            let row_doc = grid_row.doc || {};
            let $row = $(grid_row.wrapper || grid_row.row || grid_row.$row);

            let lt25_tooltip = row_doc.lt25_batches_tooltip || "No batch below 25% shelf life";
            let gt25_tooltip = row_doc.gt25_batches_tooltip || "No batch greater than 25% shelf life";
            let expiry_tooltip = row_doc.expiry_batches_tooltip || "No expired batch";

            set_custom_tooltip(
                $row.find('[data-fieldname="lt25_qty"], [data-fieldname="lt25_qty"] input'),
                lt25_tooltip,
                "batch-tooltip-lt25"
            );

            set_custom_tooltip(
                $row.find('[data-fieldname="gt25_qty"], [data-fieldname="gt25_qty"] input'),
                gt25_tooltip,
                "batch-tooltip-gt25"
            );

            set_custom_tooltip(
                $row.find('[data-fieldname="rejected_qty"], [data-fieldname="rejected_qty"] input'),
                expiry_tooltip,
                "batch-tooltip-expiry"
            );
        });
    }, 500);
}


// ========================================================
// SET custom_rejected_qty YES / NO
// ========================================================

async function check_shelf_and_set(frm) {
    let issue = await has_shelf_issue(frm);

    if (issue) {
        await frm.set_value("custom_rejected_qty", "Yes");
    } else {
        await frm.set_value("custom_rejected_qty", "No");
    }

    frm.refresh_field("custom_rejected_qty");
}


async function has_shelf_issue(frm) {
    const today = frappe.datetime.get_today();

    for (let item of frm.doc.items || []) {

        // CASE 1: Serial and Batch Bundle
        if (item.serial_and_batch_bundle) {
            let sbb = await frappe.db.get_doc(
                "Serial and Batch Bundle",
                item.serial_and_batch_bundle
            );

            let shelf_days = flt(sbb.custom_shelf_life_in_days || 0);

            if (!shelf_days) {
                shelf_days = await get_item_shelf_life_days(item.item_code);
            }

            for (let entry of (sbb.entries || [])) {
                if (!entry.batch_no || !entry.qty) continue;
                if (flt(entry.qty) < 0) continue;

                let batch = await frappe.db.get_value("Batch", entry.batch_no, "expiry_date");
                let expiry_date = batch?.message?.expiry_date;

                if (expiry_date && expiry_date < today) {
                    return true;
                }

                let remaining = await get_remaining_shelf_life(entry.batch_no);
                let percent = shelf_days ? (remaining / shelf_days) * 100 : 0;

                if (percent < 25) {
                    return true;
                }
            }
        }

        // CASE 2: Direct batch_no field
        else if (item.use_serial_batch_fields && item.batch_no) {
            let batch_doc = await frappe.db.get_doc("Batch", item.batch_no);

            let expiry_date = batch_doc?.expiry_date;

            if (expiry_date && expiry_date < today) {
                return true;
            }

            let shelf_days = await get_item_shelf_life_days(item.item_code);
            let remaining = await get_remaining_shelf_life(item.batch_no);
            let percent = shelf_days ? (remaining / shelf_days) * 100 : 0;

            if (percent < 25) {
                return true;
            }
        }
    }

    return false;
}


// ========================================================
// MAIN REVIEW FUNCTION
// ========================================================

async function calculate_accept_reject(frm) {
    const today = frappe.datetime.get_today();

    let dialog_data = [];
    let has_issue = false;

    for (let item of frm.doc.items || []) {
        if (!item.serial_and_batch_bundle) continue;

        let accepted_qty = 0;
        let rejected_qty = 0;
        let lt25_qty = 0;
        let gt25_qty = 0;

        let expired_batches = [];
        let lt25_batches = [];
        let gt25_batches = [];

        let sbb = await frappe.db.get_doc(
            "Serial and Batch Bundle",
            item.serial_and_batch_bundle
        );

        let shelf_days = flt(sbb.custom_shelf_life_in_days || 0);

        if (!shelf_days) {
            shelf_days = await get_item_shelf_life_days(item.item_code);
        }

        for (let entry of sbb.entries || []) {
            if (!entry.batch_no || !entry.qty) continue;
            if (flt(entry.qty) < 0) continue;

            let entry_qty = flt(entry.qty);

            let batch = await frappe.db.get_value(
                "Batch",
                entry.batch_no,
                "expiry_date"
            );

            let expiry_date = batch?.message?.expiry_date;

            if (expiry_date && expiry_date < today) {
                rejected_qty += entry_qty;

                expired_batches.push({
                    batch_no: entry.batch_no,
                    qty: entry_qty,
                    expiry_date: expiry_date
                });

                continue;
            }

            accepted_qty += entry_qty;

            let remaining = await get_remaining_shelf_life(entry.batch_no);
            let percent = shelf_days ? (remaining / shelf_days) * 100 : 0;
            let rounded_percent = flt(percent, 2);

            if (percent < 25) {
                lt25_qty += entry_qty;

                lt25_batches.push({
                    batch_no: entry.batch_no,
                    qty: entry_qty,
                    expiry_date: expiry_date || "",
                    remaining_shelf_life: remaining,
                    percent: rounded_percent
                });

            } else {
                gt25_qty += entry_qty;

                gt25_batches.push({
                    batch_no: entry.batch_no,
                    qty: entry_qty,
                    expiry_date: expiry_date || "",
                    remaining_shelf_life: remaining,
                    percent: rounded_percent
                });
            }
        }

        dialog_data.push({
            item_code: item.item_code,
            serial_and_batch_bundle: item.serial_and_batch_bundle,
            lt25_qty: lt25_qty,
            gt25_qty: gt25_qty,
            accepted_qty: accepted_qty,
            rejected_qty: rejected_qty,

            lt25_batches_tooltip: make_batch_tooltip(lt25_batches),
            gt25_batches_tooltip: make_batch_tooltip(gt25_batches),
            expiry_batches_tooltip: make_batch_tooltip(expired_batches)
        });

        if (rejected_qty > 0 || lt25_qty > 0) {
            has_issue = true;
        }
    }

    open_result_dialog(dialog_data, frm, has_issue);

    return !has_issue;
}


// ========================================================
// DIALOG - DYNAMIC BUTTON
// ========================================================

async function open_result_dialog(data, frm, has_issue) {
    let d = new frappe.ui.Dialog({
        title: has_issue ? "Review Items" : "Approve Items",
        size: "large",

        fields: [
            {
                fieldname: "items",
                fieldtype: "Table",
                cannot_add_rows: true,
                cannot_delete_rows: true,
                in_place_edit: false,
                data: data,
                fields: [
                    {
                        fieldname: "item_code",
                        fieldtype: "Data",
                        label: "Item",
                        in_list_view: 1,
                        read_only: 1
                    },
                    {
                        fieldname: "lt25_qty",
                        fieldtype: "Float",
                        label: "Shelf Life Less Than 25% QTY",
                        in_list_view: 1,
                        read_only: 1
                    },
                    {
                        fieldname: "gt25_qty",
                        fieldtype: "Float",
                        label: "Shelf Life Greater Than 25% QTY",
                        in_list_view: 1,
                        read_only: 1
                    },
                    {
                        fieldname: "accepted_qty",
                        fieldtype: "Float",
                        label: "Accepted QTY",
                        in_list_view: 1,
                        read_only: 1
                    },
                    {
                        fieldname: "rejected_qty",
                        fieldtype: "Float",
                        label: "Expiry QTY",
                        in_list_view: 1,
                        read_only: 1
                    },
                    {
                        fieldname: "serial_and_batch_bundle",
                        fieldtype: "Link",
                        label: "Serial and Batch Bundle",
                        options: "Serial and Batch Bundle",
                        in_list_view: 1,
                        read_only: 1
                    },

                    // Hidden tooltip fields
                    {
                        fieldname: "lt25_batches_tooltip",
                        fieldtype: "Small Text",
                        hidden: 1
                    },
                    {
                        fieldname: "gt25_batches_tooltip",
                        fieldtype: "Small Text",
                        hidden: 1
                    },
                    {
                        fieldname: "expiry_batches_tooltip",
                        fieldtype: "Small Text",
                        hidden: 1
                    }
                ]
            }
        ],

        primary_action_label: has_issue ? "Send for Approval" : "Approve",

        primary_action: async function () {
            d.hide();

            try {
                if (has_issue) {
                    frm.set_value('workflow_state', 'Purchase Team Approval Pending');
                    await frm.save();

                    frappe.show_alert({
                        message: __("Sent for approval successfully"),
                        indicator: "green"
                    });
                } else {
                    frm.set_value('workflow_state', 'Complete GRN');
                    await frm.save();

                    frappe.show_alert({
                        message: __("Approved successfully"),
                        indicator: "green"
                    });
                }

                frm.reload_doc();

            } catch (e) {
                console.error("Error:", e);

                frappe.msgprint({
                    title: __("Error"),
                    message: e.message || __("Something went wrong"),
                    indicator: "red"
                });
            }
        }
    });

    d.show();

    d.fields_dict.items.grid.refresh();

    apply_batch_hover_tooltips(d);

    $(d.$wrapper).find('.modal-dialog').css({
        "max-width": "1500px",
        "width": "100%"
    });
}


// ========================================================
// PURCHASE TEAM REVIEW FUNCTION
// ========================================================

async function calculate_accept_reject1(frm) {
    const today = frappe.datetime.get_today();

    let dialog_data = [];
    let has_rejected_items = false;

    for (let item of frm.doc.items || []) {
        if (!item.serial_and_batch_bundle) continue;

        let accepted_qty = 0;
        let rejected_qty = 0;
        let lt25_qty = 0;
        let gt25_qty = 0;

        let expired_batches = [];
        let lt25_batches = [];
        let gt25_batches = [];

        let sbb = await frappe.db.get_doc(
            "Serial and Batch Bundle",
            item.serial_and_batch_bundle
        );

        let shelf_days = flt(sbb.custom_shelf_life_in_days || 0);

        if (!shelf_days) {
            shelf_days = await get_item_shelf_life_days(item.item_code);
        }

        for (let entry of sbb.entries || []) {
            if (!entry.batch_no || !entry.qty) continue;
            if (flt(entry.qty) < 0) continue;

            let entry_qty = flt(entry.qty);

            let batch = await frappe.db.get_value(
                "Batch",
                entry.batch_no,
                "expiry_date"
            );

            let expiry_date = batch?.message?.expiry_date;

            if (expiry_date && expiry_date < today) {
                rejected_qty += entry_qty;

                expired_batches.push({
                    batch_no: entry.batch_no,
                    qty: entry_qty,
                    expiry_date: expiry_date
                });

                continue;
            }

            accepted_qty += entry_qty;

            let remaining = await get_remaining_shelf_life(entry.batch_no);
            let percent = shelf_days ? (remaining / shelf_days) * 100 : 0;
            let rounded_percent = flt(percent, 2);

            if (percent < 25) {
                lt25_qty += entry_qty;

                lt25_batches.push({
                    batch_no: entry.batch_no,
                    qty: entry_qty,
                    expiry_date: expiry_date || "",
                    remaining_shelf_life: remaining,
                    percent: rounded_percent
                });

            } else {
                gt25_qty += entry_qty;

                gt25_batches.push({
                    batch_no: entry.batch_no,
                    qty: entry_qty,
                    expiry_date: expiry_date || "",
                    remaining_shelf_life: remaining,
                    percent: rounded_percent
                });
            }
        }

        if (rejected_qty > 0) {
            has_rejected_items = true;
        }

        dialog_data.push({
            name: item.item_name,
            item_code: item.item_code,
            item_name: item.name,
            lt25_qty: lt25_qty,
            gt25_qty: gt25_qty,
            accepted_qty: accepted_qty,
            rejected_qty: rejected_qty,
            serial_and_batch_bundle: item.serial_and_batch_bundle,

            lt25_batches_tooltip: make_batch_tooltip(lt25_batches),
            gt25_batches_tooltip: make_batch_tooltip(gt25_batches),
            expiry_batches_tooltip: make_batch_tooltip(expired_batches)
        });
    }

    open_result_dialog1(dialog_data, frm, has_rejected_items);
}


function open_result_dialog1(data, frm, has_rejected_items) {
    let dialog_fields = [];

    if (has_rejected_items) {
        dialog_fields.push({
            fieldname: "rejected_warehouse",
            fieldtype: "Link",
            label: "Rejected Warehouse",
            options: "Warehouse",
            reqd: 1,
            description: "Select warehouse for rejected batches"
        });

        dialog_fields.push({
            fieldname: "section_break",
            fieldtype: "Section Break"
        });
    }

    dialog_fields.push({
        fieldname: "items",
        fieldtype: "Table",
        label: "Item Summary",
        cannot_add_rows: true,
        in_place_edit: false,
        fields: [
            {
                fieldname: "name",
                fieldtype: "Data",
                label: "Item Name",
                in_list_view: 1,
                read_only: 1
            },
            {
                fieldname: "item_code",
                fieldtype: "Data",
                label: "Item Code",
                read_only: 1
            },
            {
                fieldname: "lt25_qty",
                fieldtype: "Float",
                label: "Shelf Life Less Than 25% QTY",
                in_list_view: 1,
                read_only: 1
            },
            {
                fieldname: "gt25_qty",
                fieldtype: "Float",
                label: "Shelf Life Greater Than 25% QTY",
                in_list_view: 1,
                read_only: 1
            },
            {
                fieldname: "accepted_qty",
                fieldtype: "Float",
                label: "Accepted Total Qty",
                in_list_view: 1,
                read_only: 1
            },
            {
                fieldname: "rejected_qty",
                fieldtype: "Float",
                label: "Expiry Qty",
                in_list_view: 1,
                read_only: 1
            },
            {
                fieldname: "serial_and_batch_bundle",
                fieldtype: "Link",
                label: "Serial and Batch Bundle",
                options: "Serial and Batch Bundle",
                read_only: 1
            },

            // Hidden tooltip fields
            {
                fieldname: "lt25_batches_tooltip",
                fieldtype: "Small Text",
                hidden: 1
            },
            {
                fieldname: "gt25_batches_tooltip",
                fieldtype: "Small Text",
                hidden: 1
            },
            {
                fieldname: "expiry_batches_tooltip",
                fieldtype: "Small Text",
                hidden: 1
            }
        ]
    });

    let d = new frappe.ui.Dialog({
        title: "Accepted / Rejected Qty (Expiry Based)",
        size: "large",
        fields: dialog_fields,

        primary_action_label: "Approve",
        primary_action: async function () {
            await process_split_batches(d, frm, "Approved", has_rejected_items);
        },

        secondary_action_label: "Reject",
        secondary_action: async function () {
            await process_split_batches(d, frm, "Rejected", has_rejected_items);
        }
    });

    d.show();

    d.fields_dict.items.df.data = data;
    d.fields_dict.items.grid.refresh();

    apply_batch_hover_tooltips(d);

    $(d.$wrapper).find('.modal-dialog').css({
        "max-width": "1500px",
        "width": "100%"
    });
}


async function process_split_batches(dialog, frm, workflow_status, has_rejected_items) {
    let values = dialog.get_values();

    if (workflow_status === "Approved" && has_rejected_items && !values.rejected_warehouse) {
        frappe.msgprint({
            title: __("Required"),
            message: __("Please select Rejected Warehouse"),
            indicator: "red"
        });
        return;
    }

    dialog.hide();

    if (workflow_status === "Rejected") {
        frappe.show_alert({
            message: __("Processing..."),
            indicator: "blue"
        });

        try {
            await frappe.call({
                method: "frappe.client.set_value",
                args: {
                    doctype: frm.doc.doctype,
                    name: frm.doc.name,
                    fieldname: "workflow_state",
                    value: "Rejected By Purchase Team"
                }
            });

            frappe.show_alert({
                message: __("Rejected successfully!"),
                indicator: "orange"
            });

            frm.reload_doc();

        } catch (error) {
            frappe.msgprint({
                title: __("Error"),
                message: error.message || __("Failed to reject"),
                indicator: "red"
            });
        }

        return;
    }

    if (!has_rejected_items) {
        frappe.show_alert({
            message: __("Processing..."),
            indicator: "blue"
        });

        try {
            await frappe.call({
                method: "frappe.client.set_value",
                args: {
                    doctype: frm.doc.doctype,
                    name: frm.doc.name,
                    fieldname: "workflow_state",
                    value: "Approved"
                }
            });

            frappe.show_alert({
                message: __("Approved successfully!"),
                indicator: "green"
            });

            frm.reload_doc();

        } catch (error) {
            frappe.msgprint({
                title: __("Error"),
                message: error.message || __("Failed to update workflow"),
                indicator: "red"
            });
        }

        return;
    }

    frappe.show_alert({
        message: __("Processing..."),
        indicator: "blue"
    });

    try {
        let result = await frappe.call({
            method: "mohan_impex.purchase_receipt.split_rejected_batches",
            args: {
                pr_name: frm.doc.name,
                rejected_warehouse: values.rejected_warehouse || null,
                workflow_status: workflow_status
            }
        });

        if (result.message) {
            for (let item_name in result.message) {
                let item_row = frm.doc.items.find(
                    i => i.name === item_name
                );

                if (item_row) {
                    frappe.model.set_value(
                        item_row.doctype,
                        item_row.name,
                        "rejected_serial_and_batch_bundle",
                        result.message[item_name].rejected_bundle
                    );

                    frappe.model.set_value(
                        item_row.doctype,
                        item_row.name,
                        "rejected_warehouse",
                        result.message[item_name].rejected_warehouse
                    );
                }
            }

            if (result.message.workflow_status) {
                frm.set_value("workflow_state", result.message.workflow_status);
            }

            frm.refresh_field("items");

            frappe.show_alert({
                message: __("Approved successfully!"),
                indicator: "green"
            });

            frm.reload_doc();
        }

    } catch (error) {
        frappe.msgprint({
            title: __("Error"),
            message: error.message || __("Failed to process"),
            indicator: "red"
        });
    }
}