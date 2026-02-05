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
                        fieldname: 'item_code',
                        label: __('Item Code'),
                        options: 'Item',
                        in_list_view: 1,
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

	// preload Blanket Order items
	dialog.fields_dict.items.df.data = (frm.doc.items || []).map(row => ({
        name: row.name,
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
		method: 'mohan_impex.utils.blanket_order.update_items',
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
