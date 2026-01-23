frappe.ui.form.on('Shift Type', {
    refresh: function(frm) {
        // Add custom button for Leave Deduction
        if (!frm.is_new()) {
            frm.add_custom_button(__('Process Leave Deduction'), function() {
                frappe.call({
                    method: 'mohan_impex.leave_deduction.process_shift_leave_deduction',
                    args: {
                        shift_name: frm.doc.name
                    },
                    freeze: true,
                    freeze_message: __('Processing Leave Deduction... Please wait.'),
                    callback: function(r) {
                        // Success message already shown by server
                        frm.reload_doc();
                    },
                    error: function(r) {
                        frappe.msgprint({
                            title: __('Error'),
                            indicator: 'red',
                            message: __('Failed to process leave deduction. Please check error log.')
                        });
                    }
                });
            },);
        }
    }
});
