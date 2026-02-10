frappe.ui.form.on("Blanket Order", {
	refresh(frm) {
		set_item_code_filter(frm);
		add_hold_close_buttons_with_justification(frm);
	}
});

function add_hold_close_buttons_with_justification(frm) {
	if (frm.doc.docstatus !== 1) return;
	if (!frm.has_perm("submit")) return;

	const status = frm.doc.status || "";
	const per_delivered = flt(frm.doc.per_delivered);
	const per_billed = flt(frm.doc.per_billed);

	const is_closed_or_completed = ["Closed", "Completed"].includes(status);
	const is_pending = per_delivered < 100 || per_billed < 100;

	if (status === "On Hold") {
		frm.add_custom_button(__("Resume"), () => frm.cscript.update_status("Resume", "Draft"), __("Status"));
		if (is_pending) add_close_with_justification(frm);
		return;
	}

	if (status === "Closed") {
		frm.add_custom_button(__("Re-open"), () => frm.cscript.update_status("Re-open", "Draft"), __("Status"));
		return;
	}

	if (!is_closed_or_completed && is_pending) {
		add_hold_with_justification(frm);
		add_close_with_justification(frm);
	}
}

function add_hold_with_justification(frm) {
	frm.add_custom_button(
		__("Hold"),
		() => {
			const d = new frappe.ui.Dialog({
				title: __("Hold Blanket Order"),
				fields: [
					{
						fieldname: "justification",
						label: __("Justification"),
						fieldtype: "Link",
						options: "Justification",
						reqd: 1,
						get_query() {
							return { filters: { hold_bo: 1 } };
						},
					},
					{
						fieldname: "remarks",
						label: __("Remarks"),
						fieldtype: "Small Text",
						reqd: 1,
					},
				],
				primary_action_label: __("Confirm Hold"),
				primary_action(values) {
					if (!values || !values.justification || !values.remarks) return;

					const justification = values.justification;
					const remarks = values.remarks;

					frappe.call({
						method: "frappe.desk.form.utils.add_comment",
						args: {
							reference_doctype: frm.doctype,
							reference_name: frm.doc.name,
							content:
								"<div>" +
								"<span style='color:#d97706; font-weight:600;'>" +
								__("Reason for hold:") +
								"</span> " +
								frappe.utils.escape_html(justification) +
								"</div>" +
								"<div>" +
								"<span style='color:#1f2937; font-weight:600;'>" +
								__("Remarks:") +
								"</span> " +
								frappe.utils.escape_html(remarks) +
								"</div>",
							comment_email: frappe.session.user,
							comment_by: frappe.session.user_fullname,
						},
						freeze: true,
						freeze_message: __("Adding comment..."),
						callback(r) {
							if (r.exc) return;

							frappe.call({
								method: "erpnext.selling.doctype.blanket_order.sales_order.update_status",
								args: {
									status: "On Hold",
									name: frm.doc.name,
								},
								freeze: true,
								freeze_message: __("Putting Blanket Order on Hold..."),
								callback(rr) {
									if (rr.exc) return;

									frappe.show_alert({
										message: __("Sales Blanket is now On Hold"),
										indicator: "green",
									});
									d.hide();
									frm.reload_doc();
								},
							});
						},
					});
				},
			});

			d.show();
		},
		__("Status")
	);
}

function add_close_with_justification(frm) {
	frm.add_custom_button(
		__("Close"),
		() => {
			const d = new frappe.ui.Dialog({
				title: __("Close Blanket Order"),
				fields: [
					{
						fieldname: "justification",
						label: __("Justification"),
						fieldtype: "Link",
						options: "Justification",
						reqd: 1,
						get_query() {
							return { filters: { close_bo: 1 } };
						},
					},
					{
						fieldname: "remarks",
						label: __("Remarks"),
						fieldtype: "Small Text",
						reqd: 1,
					},
				],
				primary_action_label: __("Confirm Close"),
				primary_action(values) {
					if (!values || !values.justification || !values.remarks) return;

					const justification = values.justification;
					const remarks = values.remarks;

					frappe.call({
						method: "frappe.desk.form.utils.add_comment",
						args: {
							reference_doctype: frm.doctype,
							reference_name: frm.doc.name,
							content:
								"<div>" +
								"<span style='color:#dc2626; font-weight:600;'>" +
								__("Reason for close:") +
								"</span> " +
								frappe.utils.escape_html(justification) +
								"</div>" +
								"<div>" +
								"<span style='color:#1f2937; font-weight:600;'>" +
								__("Remarks:") +
								"</span> " +
								frappe.utils.escape_html(remarks) +
								"</div>",
							comment_email: frappe.session.user,
							comment_by: frappe.session.user_fullname,
						},
						freeze: true,
						freeze_message: __("Adding comment..."),
						callback(r) {
							if (r.exc) return;

							frappe.call({
								method: "erpnext.selling.doctype.blanket_order.sales_order.update_status",
								args: {
									status: "Closed",
									name: frm.doc.name,
								},
								freeze: true,
								freeze_message: __("Closing Blanket Order..."),
								callback(rr) {
									if (rr.exc) return;

									frappe.show_alert({
										message: __("Blanket Order is now Closed"),
										indicator: "green",
									});
									d.hide();
									frm.reload_doc();
								},
							});
						},
					});
				},
			});

			d.show();
		},
		__("Status")
	);
}


frappe.ui.form.on('Blanket Order', {
	refresh(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__('Update Items'), () => {
				open_update_items_dialog(frm);
			});
		}
	}
});

function open_update_items_dialog(frm) {
	const dialog = new frappe.ui.Dialog({
		title: __('Update Items'),
		size: 'large',
		fields: [
			{
				fieldtype: 'Date',
				fieldname: 'from_date',
				label: __('From Date'),
				reqd: 1,
				default: frm.doc.from_date
			},
			{
				fieldtype: 'Section Break'
			},
			{
				fieldtype: 'Table',
				fieldname: 'items',
				label: __('Items'),
				in_place_edit: true,
				cannot_add_rows: true,
				fields: [
					{
						fieldtype: 'Link',
						fieldname: 'item_template',
						label: __('Item Template'),
						options: 'Item',
						read_only: 1,
						in_list_view: 1
					},
					{
                        fieldtype: 'Link',
                        fieldname: 'item_code',
                        label: __('Item Code'),
                        options: 'Item',
                        in_list_view: 1,
                        get_query() {
                            const rows = dialog.fields_dict.items.df.data;
                            
                            for (let row of rows) {
                                if (!row.item_code) {
                                    
                                    return {
                						filters: [
                							["has_variants", "=", 0],
                							["is_sales_item", "=", 1],
                							["variant_of", "=", row.item_template]
                						]
                					};
                            	}
                            }
                        },
                        onchange() {
                            const row = this.grid_row.doc;
                            if (row.item_code) {
                                frappe.db.get_value('Item', row.item_code, 'item_name')
                                    .then(r => {
                                        row.item_name = r.message.item_name;
                                        this.grid.refresh();
                                    });
                            }
                        }
                    },
					{
						fieldtype: 'Data',
						fieldname: 'item_name',
						label: __('Item Name'),
						read_only: 1,
						in_list_view: 1
					},
					{
						fieldtype: 'Float',
						fieldname: 'qty',
						label: __('Quantity'),
						in_list_view: 1
					},
					{
						fieldtype: 'Currency',
						fieldname: 'rate',
						label: __('Rate'),
						in_list_view: 1
					},
					{
						fieldtype: 'Float',
						fieldname: 'ordered_qty',
						label: __('Ordered Quantity'),
						read_only: 1,
						in_list_view: 1
					}
				]
			}
		],
		primary_action_label: __('Update'),
		primary_action(values) {
			from_date = values.from_date;
			items = values.items
			update_blanket_order_items(frm,from_date, items);
			dialog.hide();
		}
	});

	dialog.fields_dict.items.df.data = (frm.doc.items || []).map(row => ({
        name: row.name,
        item_template: row.custom_item_template,
        item_code: row.item_code,
        item_name: row.item_name,
        qty: row.qty,
        rate: row.rate,
        ordered_qty: row.ordered_qty || 0
    }));


	dialog.fields_dict.items.refresh();
	dialog.show();
}

function update_blanket_order_items(frm, from_date, items) {
	frappe.call({
		method: 'mohan_impex.api.blanket_order.update_items',
		args: {
			blanket_order: frm.doc.name,
			from_date: from_date,
			items: items
		},
		callback() {
			frappe.msgprint(__('Blanket Order updated successfully'));
			frm.reload_doc();
		}
	});
}
