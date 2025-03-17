frappe.listview_settings['Request for Quotation'] = {
    onload: function(listview) {
        frappe.call({
            method: "mohan_impex.supplier_item.get_supplier_portal_users",
            args: {
                user_email: frappe.session.user // Get the logged-in user's email
            },
            callback: function(response) {
                if (response.message && response.message.length > 0) {
                    let user_supplier = response.message[0].supplier; // Get supplier name
                    frappe.set_route("List", "Request for Quotation", { 
                        "supplier": ["=", user_supplier]
                    });
                }
            }
        });
    }
};