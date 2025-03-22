frappe.ui.form.on("Sales Order", {
    customer: function(frm) {
        // Reset approval status while balance is being checked
        frm.set_value("custom_accounts_approval_status", "");

        if (frm.doc.company && frm.doc.customer) {
            frappe.call({
                method: "erpnext.accounts.utils.get_balance_on",
                args: {
                    party_type: "Customer",
                    party: frm.doc.customer,
                    company: frm.doc.company
                },
                callback: function(r) {
                    if (!r.exc && r.message != null) {
                        const balance = r.message;

                        if (balance > 0) {
                            frm.set_value("custom_accounts_approval_status", "Pending");
                            frappe.msgprint({
                                title: __("Outstanding Balance Alert"),
                                message: __("Customer has an outstanding balance of {0}. Approval from the Accounts team is required to proceed.",
                                    [frappe.format(balance, { fieldtype: "Currency" })]),
                                indicator: "red"
                            });
                        } else {
                            frm.set_value("custom_accounts_approval_status", "Approved");
                        }
                    } else {
                        frappe.msgprint({
                            title: __("Error"),
                            message: __("Could not fetch customer balance. Please try again."),
                            indicator: "red"
                        });
                        console.error("Balance fetch error:", r);
                    }
                }
            });
        }
    },

    refresh: function(frm) {
        // Show Approve/Reject buttons only if user is in Accounts and the doc is not submitted
        if (!frm.is_new() && frm.doc.docstatus === 0 &&
            ["", "Pending"].includes(frm.doc.custom_accounts_approval_status) &&
            (frappe.user.has_role("Accounts User") || frappe.user.has_role("Accounts Manager"))) {

            frm.add_custom_button("Approve", function () {
                frm.set_value("custom_accounts_approval_status", "Approved");
                frappe.msgprint(__("Sales Order approved by Accounts Team."));
                frm.save(); // Save the document
            }, __("Accounts Team Approval"));

            frm.add_custom_button("Reject", function () {
                frm.set_value("custom_accounts_approval_status", "Rejected");
                frappe.msgprint(__("Sales Order rejected by Accounts Team."));
                frm.save(); // Save the document
            }, __("Accounts Team Approval"));
        }
    },

    before_submit: function(frm) {
        const status = frm.doc.custom_accounts_approval_status;

        if (!status || ["Pending", "Rejected"].includes(status)) {
            frappe.throw(__("This Sales Order cannot be submitted. Approval Status is '{0}'. Please get approval from the Accounts team.", [status || "Not Set"]));
        }
    }
});
