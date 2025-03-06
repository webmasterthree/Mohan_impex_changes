// frappe.ui.form.on('Employee', {
//     custom_eligible_for_work_from_home: function (frm) {
//         frm.toggle_display('custom_wfh_approver', frm.doc.custom_eligible_for_work_from_home === "Yes");
//     }
// });

frappe.ui.form.on('Employee', {
    setup: function (frm) {
        // Ensure correct visibility when the form is first loaded
        toggle_custom_wfh_approver(frm);
    },
    custom_eligible_for_work_from_home: function (frm) {
        // Update visibility when the field value changes
        toggle_custom_wfh_approver(frm);
    }
});

function toggle_custom_wfh_approver(frm) {
    frm.toggle_display('custom_wfh_approver', frm.doc.custom_eligible_for_work_from_home === "Yes");
}

